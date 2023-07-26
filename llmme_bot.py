import config
import gmail_api as email_api
import llm_reply

def main():
    try:
        # Call the Gmail API
        service = email_api.get_service()

        botlabel_id = email_api.get_label_id_for_botlabel(service, botname=config.botname)

        messages = email_api.gmail_get_unread(service, botname=config.botname)
        # call model and respond
        for m in messages:
            f_from, f_to, f_cc, f_subject = m.get('To', config.my_email), m['From'], m.get('Cc',''), m['Subject']
            f_in_reply_to = m.get('Message-ID')
            f_references = m.get('References', f_in_reply_to)
            f_thread_id = m.get('threadId')
            f_message_id = m.get('id')
            f_answer = llm_reply.respond(f_from=f_from, f_to=f_to, f_cc=f_cc, f_subject=f_subject, f_context=m['Body'])
            email_api.gmail_create_draft(service, f_from=f_from, f_to=f_to, f_subject=f_subject,
                                         f_in_reply_to=f_in_reply_to, f_references=f_references,
                                         f_thread_id=f_thread_id, f_message_id=f_message_id,
                                         f_answer=f_answer, botlabel_id=botlabel_id)

    except email_api.HttpError as error:
        print(F'An error occurred: {error}')

if __name__ == '__main__':
    main()