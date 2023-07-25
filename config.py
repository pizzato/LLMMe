# use your personal model or any open source one
# model_name can be a Hugging Face link as below or a folder where your model reside on your machine
model_name = "facebook/opt-2.7b" # example only, shouldn't really work for email replies
# model_name = "your_space/your_model"

botname = "LLMMe"
my_name = "My Name"
my_email = "my_email@gmail.com"

response_template = f"""

=====================================================================
The response below was created automatically with {botname}
using an LLM trained with my emails. Thanks {my_name}
=====================================================================
{botname} Reply:
---

{{}}

---
"""

# You probably don't need to change this, unless you want to do something different
prompt_format = "from: {f_from}\nto: {f_to}\ncc: {f_cc}\nsubject: {f_subject}\ncontext: {f_context}"
prompt_format_with_markers = f"<|prompt|>{prompt_format}</s><|answer|>"
