import streamlit as st
import requests

# URL de votre serveur Rasa
rasa_server_url = "http://54.87.201.152:5005/webhooks/rest/webhook"

# Titre de l'application
st.title("Chatbot Interface - Rasa Server")

# Initialiser l'état de session pour conserver la conversation
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# Initialiser une variable pour gérer la zone de texte
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

# Fonction pour envoyer un message à Rasa et obtenir la réponse
def send_message(message):
    try:
        # Envoyer la requête POST au serveur Rasa
        response = requests.post(rasa_server_url, json={"sender": "user", "message": message})
        
        # Vérifier si la requête a réussi
        if response.status_code == 200:
            return response.json()  # Retourne le JSON avec la réponse
        else:
            st.error(f"Erreur : {response.status_code}. Impossible de contacter le serveur Rasa.")
            return None
    except Exception as e:
        st.error(f"Erreur lors de l'envoi de la requête : {e}")
        return None

# Afficher l'historique de la conversation en haut de la page
st.markdown("### Historique de la conversation")
if st.session_state.conversation:
    for sender, message in st.session_state.conversation:
        if sender == "Vous":
            st.markdown(f"**{sender}:** {message}")
        else:
            st.markdown(f"*{sender}:* {message}")
else:
    st.write("Aucune conversation pour le moment.")

# Zone d'entrée pour écrire le message
user_input = st.text_input("Vous : ", key="user_input")

# Quand l'utilisateur soumet un message
if st.button("Envoyer"):
    if user_input:
        # Envoyer le message et obtenir la réponse
        response = send_message(user_input)
        
        if response:
            # Ajouter le message de l'utilisateur à la conversation
            st.session_state.conversation.append(("Vous", user_input))
            
            # Ajouter la réponse du bot à la conversation
            for bot_response in response:
                st.session_state.conversation.append(("Bot", bot_response.get("text", "Pas de réponse trouvée.")))
        
        # Réinitialiser la zone de texte en modifiant la valeur de 'user_input' dans le state
        st.session_state.user_input = ""  # Réinitialiser le champ d'entrée
