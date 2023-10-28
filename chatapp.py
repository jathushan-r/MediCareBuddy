import streamlit as st 
from streamlit_chat import message
from googletrans import Translator
import requests
import os




@st.cache_resource(show_spinner=False)
def translator():
    return Translator()
    

def process_answer(query):
    pass

# Display conversation history using Streamlit messages
def display_conversation(history):
    for i in range(len(history["generated"])):
        message(history["past"][i], is_user=True, key=str(i) + "_user")
        message(history["generated"][i],key=str(i))

def main():
    
    st.title("🏥 HealthBot 🤖")
    translator = Translator()

    selected_language = st.sidebar.selectbox(
        "Select the preferred language",
        ["English", "Tamil", "Sinhala"],
        key="selected_language",
    )
    if selected_language == "Tamil":
        lang = "ta"
    elif selected_language == "Sinhala":
        lang = "si"
    else:
        lang = "en"

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

        r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": translator.translate(prompt,dest='en').text, "sender": "jathushan"})


        

        with st.spinner('please wait...'):
            for i in r.json():
                bot_message = i['text']
                bot_message = translator.translate(bot_message,dest='en').text

            response = bot_message
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()