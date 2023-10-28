from typing import Any, Text, Dict, List

from rasa_sdk.events import SlotSet,FollowupAction
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset
from datetime import datetime, timedelta
from database.database_connectivity import get_doctor_availability, search_doctors_by_name ,add_new_patient, add_new_appointment


class ActionFetchDoctorAvailability(Action):

    def name(self) -> Text:
        return "action_fetch_doctor_availability_data"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict]:   
        # Fetch slot values
        doctor_name = tracker.get_slot("doctor_name")
        appointment_day = tracker.get_slot("day")

        #Fetch data from database
        if " " in doctor_name:
            # If the user provided a full name
            first_name, last_name = doctor_name.split(" ", 1)
            availability = get_doctor_availability(first_name, last_name, appointment_day)
            self._respond_with_availability(dispatcher, availability)
        else:
            # If the user provided only one name
            doctors = search_doctors_by_name(doctor_name)
            if len(doctors) > 1:
                message = "I found multiple doctors with that name.\n"
                for doctor, specialty in doctors:
                    message += f"- {doctor.first_name} {doctor.last_name} ({specialty.name})\n"
                dispatcher.utter_message(text=message)
                return[SlotSet("doctor_name", None),FollowupAction(name = 'doctor_avaialability_form')]
            elif len(doctors) == 1:
                doctor, specialty = doctors[0]
                availability = get_doctor_availability(doctor.first_name, doctor.last_name, appointment_day)
                self._respond_with_availability(dispatcher, availability)
            else:
                dispatcher.utter_message(text="I couldn't find any doctors with that name.")
        return []

    def _respond_with_availability(self, dispatcher, availability):
        if availability:
            message = "Here are the available time slots:\n"
            for slot in availability:
                message += f"- {slot.start_time.strftime('%H:%M')} to {slot.end_time.strftime('%H:%M')} ({slot.specialty.name})\n"
        else:
            message = "No availability found.Do you want to book an appointment for another day?"
            dispatcher.utter_message(text=message)
            return[SlotSet("day", None),FollowupAction(name ='doctor_avaialability_form')]
        return []

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
        
        # ----------------- Remove this ------------------
        two_days_from_now = datetime.now() + timedelta(days=2)
        appointment_date = two_days_from_now.strftime("%Y-%m-%d")
        appointment_time = "15:00" 

        # Fetch slot values
        first_name = tracker.get_slot("firstname")
        last_name = tracker.get_slot("lastname")
        age = tracker.get_slot("age")
        phone = tracker.get_slot("phone")
        doctor_name = tracker.get_slot("doctor_name")
        #-------------- Uncomment below two line ----------------------------
        # patientID = add_new_patient(first_name, last_name, age, phone)
        # add_new_appointment(patientID, doctor_name, appointment_time,appointment_date)
        # Create the summary message
        summary = f"Here is the information you've provided:"
        summary += f"- First Name: {first_name}"
        summary += f"- Last Name: {last_name}"
        summary += f"- Age: {age}"
        summary += f"- Phone: {phone}"
        summary += f"- Appointment Date: {appointment_date}"
        summary += f"- Appointment Time: {appointment_time}"
        
        summary += "\nYour appointment has been successfully booked."

        # Send the summary message
        dispatcher.utter_message(text=summary)
        return [AllSlotsReset()]




# class ActionAddNewPatient(Action):

#     def name(self) -> Text:
#         return "action_add_new_patient"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict]:

#         # Fetch slot values
#         first_name = tracker.get_slot('firstname')
#         last_name = tracker.get_slot('lastname')
#         age = tracker.get_slot('age')
#         phone_number = tracker.get_slot('phone')

#         new_patient_added = add_new_patient(first_name, last_name, age, phone_number)
        
#         if new_patient_added:
#             dispatcher.utter_message(text="New patient has been added successfully.")
#         else:
#             dispatcher.utter_message(text="Failed to add new patient.")
#         return []

# class ActionAddNewAppointment(Action):

#     def name(self) -> Text:
#         return "action_add_new_appointment"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict]:

#         # Fetch slot values
#         patient_phone_number = tracker.get_slot('phone')
#         doctor_id = tracker.get_slot('doctor_id')
#         appointment_time = tracker.get_slot('time')

#         add_new_appointment(patient_phone_number, doctor_id, appointment_time)

#         dispatcher.utter_message(text="Your appointment has been booked successfully.")
#         return []