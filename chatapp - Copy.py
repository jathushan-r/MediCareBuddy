import streamlit as st 
from streamlit_chat import message
from googletrans import Translator
import requests
import os
import streamlit_authenticator as stauth
import apps.database as db




st.set_page_config(page_title="Hospital Chatbot", page_icon=":hospital:")
st.write("### 🏥 HealthBot 🤖")

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Display conversation history using Streamlit messages
def display_conversation(history):
    for i in range(len(history["generated"])):
        message(history["past"][i], is_user=True, key=str(i) + "_user")
        message(history["generated"][i],key=str(i))

def main(name):
    translator = Translator()  

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Please Enter Your Medical Inquiry or Question"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": translator.translate(prompt,dest='en').text, "sender": name})


        

        with st.spinner('please wait...'):
            bot_message = ""
            for i in r.json():
                bot_message = i['text']
                bot_message = translator.translate(bot_message,dest='ta').text

            response = bot_message
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    # --- USER AUTHENTICATION ---
    users = db.fetch_all_users()

    usernames = [entry['username'] for entry in users]
    names = [entry['name'] for entry in users]
    hashed_passwords = [entry['password'] for entry in users]


    authenticator = stauth.Authenticate(
        names,
        usernames,
        hashed_passwords,
        "rasa_login",
        "random_signature_key",
        30
    )

    with st.sidebar:
        name, authentication_status, username = authenticator.login("Login", "main")

    if authentication_status:
        with st.sidebar:
            authenticator.logout("logout")
        main(name)

    if authentication_status == False:
        st.error("Username/password is incorrect")

    if authentication_status == None:
        st.warning("Please enter your username and password")

    