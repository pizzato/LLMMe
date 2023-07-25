from __future__ import print_function

import base64
import os.path
from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import config

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_credentials():
    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def get_service():
    creds = get_credentials()

    try:
        # Call the Gmail API
        return build('gmail', 'v1', credentials=creds)
    except HttpError as error:
        print(F'An error occurred: {error}')

def gmail_create_draft(service, f_from, f_to, f_subject, f_in_reply_to, f_references, f_thread_id, f_message_id, f_answer, botlabel_id):

    print(f"Creating draft: {f_subject}")
    try:
        message = EmailMessage()

        message.set_content(config.response_template.format(f_answer))

        message['To'] = f_to
        message['From'] = f_from
        message['Subject'] = f_subject
        message['In-Reply-To'] = f_in_reply_to
        message['References'] = f_references
        message['threadId'] = f_thread_id

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {
            'message': {
                'threadId' : f_thread_id,
                'raw': encoded_message
            }
        }
        # pylint: disable=E1101
        draft = service.users().drafts().create(userId="me",
                                                body=create_message).execute()

        print(F'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')

        service.users().messages().modify(userId="me", id=f_message_id, body=dict(addLabelIds=[botlabel_id])).execute()

    except HttpError as error:
        print(F'An error occurred: {error}')
        draft = None

    return draft


def get_label_id_for_botlabel(service, botname):
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    for label in labels:
        if label['name'] == botname:
            return label["id"]

    # if it gets here, it needs to create
    label = service.users().labels().list(userId='me', body=dict(name=botname)).execute()
    return label['id']

def gmail_get_unread(service, botname):
    print("gmail_get_unread")
    try:
        inbox = service.users().messages().list(userId="me", q=f'in:inbox l:unread -l:{botname}').execute()

        messages_raw = []
        while True:
            messages_raw += [service.users().messages().get(userId="me",id=m['id']).execute() for m in inbox.get('messages',[])]
            if 'pageToken' in inbox:
                inbox = service.users().messages().list(userId="me", q='in:inbox', pageToken=inbox['pageToken']).execute() # untested
            else:
                break


        messages = []
        for mraw in messages_raw:
            payload = mraw['payload']
            message = {d['name']:d['value'] for d in payload['headers'] if d['name'] in ['From', 'To', 'Cc', 'Subject', 'Content-Type', 'Message-ID', 'References']}

            body_message = ""
            if (payload['body']['size'] != 0) and (message['Content-Type'].contains('text/plain')):
                body_message = payload['body']['data']
            elif 'parts' in payload and len(payload['parts']) > 0:
                for part in payload['parts']:
                    if part['mimeType'] == 'text/plain':
                        body_message = part['body']['data']

            if body_message != "":
                body_message = base64.urlsafe_b64decode(body_message).decode()

            message['Body'] = body_message
            message.pop('Content-Type')

            message['threadId'] = mraw.get('threadId','')
            message['id'] = mraw.get('id')
            messages.append(message)

        return messages

    except HttpError as error:
        print(F'An error occurred: {error}')
        return []

