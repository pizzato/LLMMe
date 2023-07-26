import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

import config

device = 'cuda' if torch.cuda.is_available() else \
         'mps' if torch.backends.mps.is_available() else \
         'cpu'

tokenizer = AutoTokenizer.from_pretrained(
    config.model_name,
    use_fast=False,
    trust_remote_code=True
)

model = AutoModelForCausalLM.from_pretrained(
    config.model_name,
    torch_dtype="auto",
    device_map="auto",
    trust_remote_code=True
)



def respond(f_from, f_to, f_cc, f_subject, f_context):
    """
        Query the LLM

    :param f_from: email From field
    :param f_to: email To field
    :param f_cc: email CC field
    :param f_subject: email Subject
    :param f_context: email context (in a reply to an email, the content of the previous email)
    :return:
    """
    print(f"Bot Respond to {f_subject}")

    message = config.prompt_format_with_markers.format(f_from=f_from, f_to=f_to, f_cc=f_cc, f_subject=f_subject, f_context=f_context[:config.max_context_length_chars])

    inputs = tokenizer(message, return_tensors="pt", add_special_tokens=False).to(device)

    # generate configuration can be modified to your needs
    tokens = model.generate(
        **inputs,
        min_new_tokens=5,
        max_new_tokens=256,
        do_sample=False,
        num_beams=2,
        temperature=float(0.3),
        repetition_penalty=float(1.5),
        renormalize_logits=True
    )[0]

    tokens = tokens[inputs["input_ids"].shape[1]:]
    answer = tokenizer.decode(tokens, skip_special_tokens=True)

    return answer

def gradio_app():
    """
     Gradio app if file is run directly as main
    """
    import gradio as gr

    with gr.Blocks(title='LLMMe') as demo:
        f_from = gr.Textbox(value=config.my_email, label="From: ")
        f_to = gr.Textbox(label="To: ")
        f_cc = gr.Textbox(label="Cc: ")
        f_subject = gr.Textbox(label="Subject: ")
        f_context = gr.Textbox(label="Context: ")
        bt_respond = gr.Button("Respond")

        gr.Markdown(value="# Bot Response")
        f_response = gr.Markdown()


        bt_respond.click(respond, [f_from, f_to, f_cc, f_subject, f_context], [f_response])

    demo.launch(debug=True)

if __name__ == "__main__":
    gradio_app()