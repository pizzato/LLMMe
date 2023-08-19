# use your personal model or any open source one
# model_name can be a Hugging Face link as below or a folder where your model reside on your machine
model_name = "facebook/opt-2.7b" # example only, shouldn't really work for email replies
# model_name = "your_space/your_model"

botname = "LLMMe"
my_name = "My Name"
my_email = "my_email@gmail.com"

max_context_length_chars = 1500

# Setting reply_automatically to true is discourage as the bot will always send the reply and won't create a draft
reply_automatically = False

response_template = f"""

{{}}

---
==============
The response above created/sent by a bot using LLMMe. 

This was: {botname} responding for {my_name}

Check out the project at https://github.com/pizzato/LLMMe
"""

# You probably don't need to change this, unless you want to do something different
prompt_format = "from: {f_from}\nto: {f_to}\ncc: {f_cc}\nsubject: {f_subject}\ncontext: {f_context}"
prompt_format_with_markers = f"<|prompt|>{prompt_format}</s><|answer|>"
