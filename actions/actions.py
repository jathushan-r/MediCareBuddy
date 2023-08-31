# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List

from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime, timedelta


class ActionSayShirtSize(Action):

    def name(self) -> Text:
        return "action_say_shirt_size"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        shirt_size = tracker.get_slot("shirt_size")
        if not shirt_size:
            dispatcher.utter_message(text="I don't know your shirt size.")
        else:
            dispatcher.utter_message(text=f"Your shirt size is {shirt_size}!")
        return []

class ActionConfirmAppointment(Action):
    def name(self):
        return "action_submit_appointment_form"

    def run(self, dispatcher, tracker, domain):

        two_days_from_now = datetime.now() + timedelta(days=2)
        appointment_date = two_days_from_now.strftime("%Y-%m-%d")
        appointment_time = "15:00" 

        # Fetch slot values
        first_name = tracker.get_slot("firstname")
        last_name = tracker.get_slot("lastname")
        age = tracker.get_slot("age")
        phone = tracker.get_slot("phone")

        # Create the summary message
        summary = f"Here is the information you've provided:\n"
        summary += f"- First Name: {first_name}\n"
        summary += f"- Last Name: {last_name}\n"
        summary += f"- Age: {age}\n"
        summary += f"- Phone: {phone}\n"
        summary += f"- Appointment Date: {appointment_date}\n"
        summary += f"- Appointment Time: {appointment_time}\n"
        
        summary += "\nYour appointment has been successfully booked."

        # Send the summary message
        dispatcher.utter_message(text=summary)