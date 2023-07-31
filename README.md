# LLMMe
Create your own LLM and use it to respond to your email (gmail only now)

This repository contains a couple of program that can be used to create your own LLM and use it to respond to your email (gmail only now).

The following steps are required to make this work:
1. Use Google Takeout to download your data from GMail.
2. After receiving the link to download, save your file and unzip it. Please note the .mbox file
4. Use the script `convert_mbox_to_csv.py` to generate a prompt/answer dataset containing all your replies with the context of the message you are replying to and the original messages you have composed. **Keep in mind that both the .mbox and .csv files will contain all your emails in an unencrypted format. You want to protect this files and do not share them online!**
   
    To run the program use: 
```bash
usage: convert_mbox_to_csv.py [-h] -i INPUT -o OUTPUT -e EMAILS [EMAILS ...]

Create email training set for LLMs.

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Mailbox file (.mbox)
  -o OUTPUT, --output OUTPUT
                        Output file (.csv)
  -e EMAILS [EMAILS ...], --emails EMAILS [EMAILS ...]
                        List of senders emails (From)
```

4. After the CSV file is created use any LLM training tool that generates an LLM compatible with [AutoModelForCausalLM](https://huggingface.co/transformers/v3.5.1/model_doc/auto.html#automodelforcausallm)

    Personally, I use [H2O's LLM Studio](https://github.com/h2oai/h2o-llmstudio) because it's a very easy to do import datasets and train an LLM on top of foundational models. 
    My personal model was successfully trained using an RTX 4080 with more than 100K email in about an hour per epoch using [/facebook/opt-2.7b](https://huggingface.co/facebook/opt-2.7b).
5. After having your model at hand. Go play with it for a bit. Change the variables to your liking on `config.py`. Specifically you need to define which model you are using here. This is your personal model directory or hugging face space/model format in case you have it uploaded there.

    Run: `python llm_reply.py` and you will have a gradio app running your model.
6. If you are happy with it, you can then enable your email bot.
   1. You need to enable the [GMail API](https://developers.google.com/gmail/api/quickstart/python) <- follow the guides
   2. Then after obtaining the `credentials.json` file, add it to this folder. Run `python llmme_bot.py` and you will get a URL to obtain a `token.json` file which will be recorded to your folder automatically.
   
### What does llm_bot.py do?

It searches for all unread messages in your inbox that have not been previously read by the bot, and creates a draft reply to that message using your personal LLM (or other of your liking). The draft message will contain a warning that comes from a bot as specified in `config.py`. This program will not send or reply to the message, it will simply create a draft reply.

In order not to redo messages, the program creates a tag with the name of your bot (e.g. "LLMMe" as in `config.py`) and tags all emails that it has created a draft for already. 

### Troubleshoot

For Mac M1/M2 as indicated in (https://github.com/pytorch/pytorch/issues/96610), run `pip3 install --upgrade --no-deps --force-reinstall --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu`.

### Add to crontab

On a Mac or Linux, just add your program to a cron job. Mine run every 1 hour!