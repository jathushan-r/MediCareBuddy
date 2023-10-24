import requests
from gtts import gTTS
from googletrans import Translator
import subprocess

bot_message = ""
message = ""

translator = Translator()
translation = translator.translate("hello").text

r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": "Hello"})

print("Bot says, ", end=' ')
for i in r.json():
    bot_message = i['text']
    print(f"{bot_message}")

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

