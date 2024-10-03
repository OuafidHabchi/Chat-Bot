import streamlit as st
import requests

# Define the URL of your Rasa server
rasa_server_url = "http://3.87.73.156:5005/webhooks/rest/webhook"

# Title of the page
st.title("Assistant Virtuel - Chatbot")

# CSS to style the chat bubbles
st.markdown("""
    <style>
    .user-bubble {
        background-color: #DCF8C6;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        max-width: 60%;
        float: right;
        clear: both;
    }
    .bot-bubble {
        background-color: #F1F0F0;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        max-width: 60%;
        float: left;
        clear: both;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize message history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Function to send a message to Rasa and get a response
def send_message_to_rasa(user_message):
    try:
        response = requests.post(rasa_server_url, json={"sender": "user", "message": user_message}, timeout=10)
        response.raise_for_status()  # Check if the HTTP request was successful
        return response.json()  # Parse the response to JSON
    except:
        return [{"text": "Erreur: le serveur Rasa est injoignable pour l'instant."}]

# Function to display messages
def display_messages():
    for message in st.session_state["messages"]:
        if message["sender"] == "user":
            st.markdown(f'<div class="user-bubble">{message["message"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-bubble">{message["message"]}</div>', unsafe_allow_html=True)

# Show the message history
display_messages()

# User input form
with st.form(key="user_input_form", clear_on_submit=True):
    user_message = st.text_input("Tapez votre message ici...")
    submit_button = st.form_submit_button("Envoyer")

# Handle form submission
if submit_button and user_message:
    # Add the user's message to the message history
    st.session_state["messages"].append({"sender": "user", "message": user_message})

    # Show the updated conversation immediately
    display_messages()

    # Get the bot's response and add it to the history
    responses = send_message_to_rasa(user_message)
    for response in responses:
        st.session_state["messages"].append({"sender": "bot", "message": response["text"]})

    # Show the updated conversation with the bot's response
    display_messages()
