import streamlit as st
import requests

# URL de votre serveur Rasa
rasa_server_url = "http://54.87.201.152:5005/webhooks/rest/webhook"

# Titre de l'application
st.title("Chatbot Interface - Rasa Server")

# Initialiser l'état de session pour conserver la conversation
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# Fonction pour envoyer un message à Rasa et obtenir la réponse
def send_message(message):
    # Envoyer la requête POST au serveur Rasa
    response = requests.post(rasa_server_url, json={"sender": "user", "message": message})
    return response.json()

# Zone d'entrée pour écrire le message
user_input = st.text_input("Vous : ", "")

# Quand l'utilisateur soumet un message
if st.button("Envoyer"):
    if user_input:
        # Envoyer le message et obtenir la réponse
        response = send_message(user_input)
        
        # Ajouter le message de l'utilisateur à la conversation
        st.session_state.conversation.append(("Vous", user_input))
        
        # Ajouter la réponse du bot à la conversation
        for bot_response in response:
            st.session_state.conversation.append(("Bot", bot_response.get("text", "")))

# Afficher l'historique de la conversation
if st.session_state.conversation:
    for sender, message in st.session_state.conversation:
        if sender == "Vous":
            st.markdown(f"**{sender}:** {message}")
        else:
            st.markdown(f"*{sender}:* {message}")
