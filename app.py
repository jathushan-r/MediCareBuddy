## Run this command in terminal  before executing this program
## rasa run -m models --endpoints endpoints.yml --port 5002 --credentials credentials.yml
## and also run this in seperate terminal
## rasa run actions


import requests
from googletrans import Translator

bot_message = ""
message = ""

translator = Translator()
translation = translator.translate("hello").text

r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": "Hello"})

print("Bot says, ", end=' ')
for i in r.json():
    bot_message = i['text']
    print(f"{translator.translate(bot_message,dest='ta').text}")

while bot_message != "Bye" or bot_message != 'thanks':
    message = input("You: ")  # Read user input as text

    if len(message) == 0:
        continue

    print("Sending message now...")

    r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": translator.translate(message,dest='en').text})

    print("Bot says, ", end=' ')
    for i in r.json():
        bot_message = i['text']
        print(f"{translator.translate(bot_message,dest='ta').text}")

