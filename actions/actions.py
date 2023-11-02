from typing import Any, Text, Dict, List
import requests
from rasa_sdk.events import SlotSet,FollowupAction,AllSlotsReset,ActionReverted,UserUtteranceReverted
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime, timedelta
from database.database_connectivity import get_doctor_availability, search_doctors_by_name ,add_new_patient,search_doctors_by_fullname, add_new_appointment
from Helpers.sendSMS import sendSMS,convert_to_desired_format,convert_to_desired_format1
from Helpers.Day_Date import get_latest_date_for_day
from database.database_connectivity import delete_appointment, get_upcoming_appointments


# Define the base URL of the API
base_url = "http://localhost:8000"  # Change this URL if your API is hosted elsewhere

# Define the base URL of the API
base_url = "http://localhost:8000"  # Change this URL if your API is hosted elsewhere

# Function to send a chat request to the API
def send_chat_request(query):
    endpoint = "/chat"
    data = {"query": query}
    response = requests.post(base_url + endpoint, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.text)
        return None


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
            doctors = search_doctors_by_fullname(first_name,last_name)
            if doctors:
                availability = get_doctor_availability(first_name, last_name, appointment_day)
                start_time,specialty = self._respond_with_availability(dispatcher, availability)
                if start_time:
                    return [SlotSet("specialty",specialty),SlotSet("start_time",start_time)]
                else:
                    return [SlotSet("day",None)]
            else:
                message = "I couldn't find any doctors with that name in this hospital.Do you still want book an appointment with another doctor?"
                # message +="Psychiatrist\n"
                # message +="Orthopedist\n"
                # message +="Pediatrician\n"
                # message +="General Physician\n"
                # message +="Dermatologist\n"
                # message +="ENT Specialist\n"
                # message +="Gastroenterologist\n"
                # message +="Cardiologist\n"
                # message +="Neurologist\n"
                # message +="Ophthalmologist"

                # events.append(ActionExecuted("action_listen"))

                #         return events
                dispatcher.utter_message(text=message)
                # dispatcher.FollowupAction(name= 'doctor_avaialability_form')
                return [SlotSet("doctor_name",None)]
        else:
            # If the user provided only one name
            doctors = search_doctors_by_name(doctor_name)
            if len(doctors) > 1:
                message = "I found multiple doctors with that name.\n"
                for doctor, specialty in doctors:
                    message += f"- {doctor.first_name} {doctor.last_name} ({specialty.name})\n"
                dispatcher.utter_message(text=message)
                return[SlotSet("doctor_name", None)]
            elif len(doctors) == 1:
                doctor, specialty = doctors[0]
                availability = get_doctor_availability(doctor.first_name, doctor.last_name, appointment_day)
                self._respond_with_availability(dispatcher, availability)
                return[SlotSet("day", None),ActionReverted()]
            else:
                message = "I couldn't find any doctors with that name in this hospital.Do you still want book an appointment with another doctor?"
                # message +="Psychiatrist\n"
                # message +="Orthopedist\n"
                # message +="Pediatrician\n"
                # message +="General Physician\n"
                # message +="Dermatologist\n"
                # message +="ENT Specialist\n"
                # message +="Gastroenterologist\n"
                # message +="Cardiologist\n"
                # message +="Neurologist\n"
                # message +="Ophthalmologist"

                dispatcher.utter_message(text=message)
                return [SlotSet("doctor",None)]
            return[]

    def _respond_with_availability(self, dispatcher, availability):
        start_time = None
        specialty = None
        if availability:
            message = "Here are the available time slots:\n"
            for slot in availability:
                specialty = slot.specialty.SpecialtyName
                start_time = slot.Start_Time
                End_time = slot.End_time
                start_time = start_time.strftime('%H:%M')
                End_time = End_time.strftime('%H:%M')
                print([specialty,start_time,End_time])
                message += f"- {start_time} to {End_time} \n"
                message += f"Do you want to book an appointment for this time slot?"
                dispatcher.utter_message(text=message)
                
        else:
            message = "No availability found.Do you want to book an appointment for another day?"
            dispatcher.utter_message(text=message)
        return[start_time,specialty]
    
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
        phone = convert_to_desired_format1(tracker.get_slot("phone"))
        doctor_name = tracker.get_slot("doctor_name")
        appointment_time = tracker.get_slot("start_time")
        # appointment_time = tracker.get_slot("start_time")
        appointment_date = get_latest_date_for_day(tracker.get_slot("day"))
        otp = tracker.get_slot("otp")
        otp_generated = tracker.get_slot("otp_generated")
        print(appointment_date)
        # otp_generated = 187608
        #-------------- Uncomment below two line ----------------------------
        if (otp == otp_generated):
            print("OTP is correct")
            patientID = add_new_patient(first_name, last_name, age, phone)
            add_new_appointment(patientID, doctor_name, appointment_time,appointment_date)
            # Create the summary message
            summary = f"Here is the information you've provided:\n"
            summary += f"- First Name: {first_name}\n"
            summary += f"- Last Name: {last_name}\n"
            summary += f"- Age: {age}\n"
            summary += f"- Phone: {phone}\n"
            summary += f"- Appointment Date: {appointment_date}\n"
            summary += f"- Appointment Time: {appointment_time}"
            summary += "\nYour appointment has been successfully booked."
            # Send the summary message
            dispatcher.utter_message(text=summary)
                # return [SlotSet("otp_generated",None),SlotSet("otp",None)]
            # return [SlotSet("otp",None)]
            return [SlotSet("otp",None)]
        else:
            dispatcher.utter_message(text="OTP is incorrect.Please try again.")
            return [SlotSet("otp",None),UserUtteranceReverted()]


class ActionSendOTP(Action):
    def name(self) -> Text:
        return "action_send_otp"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:

        # Fetch the recipient's phone number from the slot or any other method
        phone_number = convert_to_desired_format(tracker.get_slot("phone"))  # Replace with the appropriate slot name

        # Send the OTP via SMS
        otp= sendSMS(phone_number)

        # You can also store the OTP in a slot for later verification if needed
        return [SlotSet("otp_generated", otp)]
       
class ActionDeleteAppointment(Action):

    def name(self):
        return "action_delete_appointment"

    def run(self, dispatcher, tracker, domain):
        # Extract appointment details from slots or user input
        appointment_id = tracker.get_slot("appointment_id")

        if appointment_id:
            # Delete the appointment from the database
            delete_appointment(appointment_id)

            dispatcher.utter_message("Appointment has been successfully canceled.")
            return [SlotSet("appointment_id", None)]
        else:
            dispatcher.utter_message("I couldn't identify the appointment to cancel.")
            return []

class ActionListUpcomingAppointments(Action):

    def name(self):
        return "action_list_upcoming_appointments"

    def run(self, dispatcher, tracker, domain):
        # Retrieve upcoming appointments from the database
        upcoming_appointments = get_upcoming_appointments()

        if upcoming_appointments:
            message = "Here are your upcoming appointments:\n"
            for appointment in upcoming_appointments:
                message += f"- Appointment ID: {appointment.Appointment_ID}\n"
                message += f"- Doctor Name: {appointment.doctor.First_name} {appointment.doctor.Last_name}\n"
                message += f"- Appointment Date: {appointment.Appointment_day}\n"
                message += f"- Appointment Time: {appointment.Appointment_time.strftime('%H:%M')}\n"
                message += "\n"

            dispatcher.utter_message(message)
        else:
            dispatcher.utter_message("You don't have any upcoming appointments.")

        return []
    

class LLMResponseAction(Action):
    def name(self) -> Text:
        return "action_llm_response"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_input = (tracker.latest_message)['text']
        response_text = send_chat_request(user_input)
        response_text = response_text['answer'].replace('\n', ' ').replace('\r', '')
        print(response_text)
        dispatcher.utter_message(text=response_text)
        return []
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