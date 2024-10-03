import streamlit as st
import requests

# Définir l'URL du serveur Rasa
rasa_server_url = "http://3.87.73.156:5005/webhooks/rest/webhook"

# Titre de la page
st.title("Assistant Virtuel - Chatbot")

# CSS pour styliser les bulles de dialogue
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

# Initialiser l'historique des messages
if "messages" not in st.session_state:
    st.session_state["messages"] =
