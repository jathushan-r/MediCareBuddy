
import streamlit_authenticator as stauth
import streamlit as st  # pip install streamlit

import database as db


st.set_page_config(page_title="Hospital Chatbot", page_icon=":hospital:")

# --- USER AUTHENTICATION ---
users = db.fetch_all_users()

usernames = [entry['username'] for entry in users]
names = [entry['name'] for entry in users]
hashed_passwords = [entry['password'] for entry in users]


authenticator = stauth.Authenticate(
    names,
    usernames,
    hashed_passwords,
    "random_cookie_name",
    "random_signature_key",
    30
)


name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    st.markdown(f"Welcome {name}!")
    authenticator.logout("logout")