from typing import List
from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.shared.nlu.training_data.message import Message
from googletrans import Translator
translator = Translator()

from rasa.core.channels import OutputChannel, UserMessage
from rasa.core import utils

@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.INTENT_CLASSIFIER], is_trainable=False
)
class TranslateToEnglishComponent(GraphComponent):
    def __init__(self):
        self.translator = Translator()

    def process(self, messages: List[Message]) -> List[Message]:
        translated_messages = []

        for message in messages:
            user_input = message.get("text")
            translation=translator.translate(user_input, src="ta", dest='en')
            message=translation.text
            translated_message = Message(data={"text": message})
            translated_messages.append(translated_message)
        return translated_messages