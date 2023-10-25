from rasa.core.channels import OutputChannel
from googletrans import Translator

class TranslateResponseMiddleware(OutputChannel):
    def __init__(self, output_channel):
        self.translator = Translator()
        self.output_channel = output_channel

    async def send_response(self, recipient_id, message):
        # Translate the message using googletrans

        translated_message = self.translator.translate(message,src="auto", dest='ta').text

        # Send the translated message to the user using the specified output channel
        await self.output_channel.send_response(recipient_id, translated_message)