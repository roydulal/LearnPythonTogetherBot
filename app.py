import sys
from flask import Flask, request
from pprint import pprint
from pymessenger import Bot
from utils import wit_response
import json
from talk import template, talking
from gnewsclient import gnewsclient

app = Flask(__name__)

# Facebook apps link:   https://developers.facebook.com/apps/2222049801408664/dashboard/
FB_ACCESS_TOKEN = "EAAfk8UkWEJgBAIIX1hzUoRXZA4OWlh7QjLeA5nCmS9bTWzbOwyiZBUqqX9ZAWPlihNFSqBoKVtDQVx0YaR9zFtP8j8UUsLahjmvLipWAQgZBW1p6BlvMp1VlVY6INjblCUUZAAUWjJ7a4c1uGcAY6bOjPPcerFF1P2JfCKCQVdAZDZD"
bot = Bot(FB_ACCESS_TOKEN)

VERIFICATION_TOKEN = "hello"


@app.route('/', methods=['GET'])
def verify():
    # Web hook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)

    # Necessary Code that extract json data facebook send
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:

                # IDs
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']

                if messaging_event.get('message'):
                    # Extracting text message
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    else:
                        messaging_text = 'no text'

                    # replace Echo Bot to wit ai
                    response = None

                    entity, value = wit_response(messaging_text)

                    if entity == 'greetings':
                        response = 'স্বাগতম '
                        # '''{
                        #               "recipient":{
                        #                 "id":"recipient_id"
                        #               },
                        #               "message":{
                        #                 "attachment":{
                        #                   "type":"template",
                        #                   "payload":{
                        #                     "template_type":"<TEMPLATE_TYPE>",
                        #                     ...
                        #                   }
                        #                 }
                        #               }
                        #             }'''


                    if entity == 'learn_python':
                        response = 'প্রতিদিন সকাল ১০.৩০ থেকে ১১.৩০ প্রজন্ত আনলাইনে ক্লাস হয় ।  কোরতে পারলে লিখুন “ পারব ”   ।'
                    elif entity == 'agree':
                        response = 'এগুলো যোগার করুন :\n১. কথা বল ও শোনার জন্য (হেডফোন) \n২.আমরা যোগাযোগে যে সফটওয়্যার ব্যাবহার করি (Google Hangout)\nএগুলো থাকলে লিখুন আমার “ আছে ” । '
                    elif entity == 'I_have':
                        response = 'স্বাগতম আমাদের ক্লাসে ।'


                    elif entity == 'thanks':
                        response = 'আপনাকেও । আরও জানতে চাইলে যোগাযোগ করুন'

                    if response == None:
                        response = "আমি বুদ্ধীহিন বাংলা রোবট ইংরেজী বুঝি না , বাংলাও কম বুঝি, আনেক কথা থাকলে ফর্মটি পুরন করুন । একজন সত্যি মানুষ এসে উত্তর দেবে । https://docs.google.com/forms/d/1S3KzdSU-g5THykGi7RhbqE2BqLmrdWXxV9J4dOLd1HU/prefill"

                    bot.send_text_message(sender_id, response)

    return "ok", 200


def log(message):
    # previously it was print now I just Use Petty Print
    pprint(message)
    sys.stdout.flush()


if __name__ == "__main__":
    app.run(use_reloader=True)
