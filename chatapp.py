import streamlit as st 
from streamlit_chat import message
from googletrans import Translator
import requests
import os
import streamlit_authenticator as stauth
import database.database as db
import time

st.set_page_config(page_title="Hospital Chatbot", page_icon=":hospital:")

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

if 'translator' not in st.session_state:
    st.session_state.translator = Translator()

if 'user' not in st.session_state:
    st.session_state.user = None

if 'selected_language' not in st.session_state:
    st.session_state.selected_language = "en"

if 'start' not in st.session_state:
    st.session_state.start = False

def initialize_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_chat_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def send_user_message(prompt, name):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

def send_assistant_message(response):
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

def clear_chat():
    st.session_state.messages = []  # Clear the chat history

def main(name):
    initialize_chat_history()
    display_chat_messages()

    if prompt := st.chat_input("Please Enter Your Medical Inquiry or Question"):
        send_user_message(prompt, name)

        # Translate user input
        translated_prompt = st.session_state.translator.translate(prompt, dest='en').text

        # Make a request to the assistant
        r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": translated_prompt, "sender": name})

        bot_message = ""
        for i in r.json():
            bot_message = i['text']
            bot_message = st.session_state.translator.translate(bot_message, dest=st.session_state.selected_language).text

        send_assistant_message(bot_message)


if __name__ == "__main__":
    # --- USER AUTHENTICATION ---
    # st.session_state   
    
    users = db.fetch_all_users()

    usernames = [entry['username'] for entry in users]
    names = [entry['firstname'] + entry['lastname'] for entry in users]
    hashed_passwords = [entry['password'] for entry in users]


    authenticator = stauth.Authenticate(
        names,
        usernames,
        hashed_passwords,
        "rasa_login",
        "random_signature_key",
        30
    )

    c1, c2,c3 = st.columns((2, 0.1,3))
    if 'authentication_status' not in st.session_state:
        st.session_state.authentication_status = None
    with c1:
        st.markdown('\n\n')

        if not st.session_state.authentication_status:
            st.markdown("<h1 style='text-align: center; font-size:30px;'> </h1>", unsafe_allow_html=True)
            st.markdown("<h1 style='text-align: center; font-size:50px;'> </h1>", unsafe_allow_html=True)
            st.markdown("<h1 style='text-align: center; font-size:30px;'>🏥 HealthBot 🤖</h1>", unsafe_allow_html=True)
    with c3:
        name, authentication_status, username = authenticator.login("Login", "main")

    if not st.session_state.get('authentication_status', False):
        st.session_state.pop('messages', None)

    st.session_state.user = name

    if authentication_status:      

        with st.sidebar:
            st.markdown("<h1 style='text-align: center; font-size:30px;'>🏥 HealthBot 🤖</h1>", unsafe_allow_html=True)            
            
            st.markdown("***")
           
            selected_language = st.sidebar.selectbox(
                    '$$ \\sf { {Select\ the\ Preferred\ Language}}$$ \n $$ \\sf { {කැමති\ භාෂාව\ තෝරන්න}}$$ \n $$ \\sf { \small{மொழியைத்\ தேர்ந்தெடுக்கவும்}}$$', 
                    ["English", "தமிழ்", "සිංහල"],
                    placeholder="Select contact method...",
                )
            if selected_language == "தமிழ்":
                lang = "ta"
            elif selected_language == "සිංහල":
                lang = "si"
            else:
                lang = "en"
            st.session_state.selected_language = lang


        with st.sidebar:
            st.markdown('***')       

            col11, col21, col31 = st.sidebar.columns((1, 3, 1))
            with col21:
                if st.button('notifications'):
                    st.toast('find the egg',icon='🥚')
                    time.sleep(.5)
                    st.toast('fry it', icon='🍳')
                    time.sleep(.5)
                    st.toast('ENJOY THE MEAL!', icon='😋')


                if st.button("Clear Chat"):
                    clear_chat()  # Clear chat history when the "Clear Chat" button is clicked
                authenticator.logout("🔒 logout")
        
        main(name)

    if authentication_status == False:
        st.error("Username/password is incorrect ❌")

    if authentication_status == None:
        c1,c3, c2 = st.columns((2,0.2, 3))
        with c2:
            st.info("Please enter your username and password 🔐")


     

    