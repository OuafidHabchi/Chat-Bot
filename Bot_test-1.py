import streamlit as st
import requests

# Définir l'URL du serveur Rasa
rasa_server_url = "http://54.87.201.152:5005/webhooks/rest/webhook"

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
    st.session_state["messages"] = []

# Fonction pour envoyer un message à Rasa et obtenir une réponse
def send_message_to_rasa(user_message):
    try:
        response = requests.post(rasa_server_url, json={"sender": "user", "message": user_message})
        response.raise_for_status()  # Vérifie si la réponse HTTP est une erreur
        return response.json()  # Tente de parser la réponse en JSON
    except requests.exceptions.ConnectionError:
        return [{"text": "Impossible de se connecter au serveur Rasa. Assurez-vous qu'il est bien démarré."}]
    except requests.exceptions.RequestException as e:
        return [{"text": f"Une erreur HTTP s'est produite : {e}"}]
    except ValueError:
        return [{"text": "La réponse du serveur n'était pas au format JSON."}]

# Afficher les messages échangés
for message in st.session_state["messages"]:
    if message["sender"] == "user":
        st.markdown(f'<div class="user-bubble">{message["message"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-bubble">{message["message"]}</div>', unsafe_allow_html=True)

# Utilisation de `st.form` pour la saisie des messages utilisateur
with st.form(key="user_input_form", clear_on_submit=True):
    user_message = st.text_input("Tapez votre message ici...")
    submit_button = st.form_submit_button("Envoyer")

# Si l'utilisateur soumet un message
if submit_button and user_message:
    # Ajouter le message utilisateur à l'historique
    st.session_state["messages"].append({"sender": "user", "message": user_message})

    # Envoyer le message à Rasa et obtenir la réponse
    responses = send_message_to_rasa(user_message)

    # Afficher la réponse brute pour déboguer
    st.write(responses)  # Décommenter pour voir la réponse brute

    # Ajouter la réponse du bot à l'historique après réception de la réponse
    for response in responses:
        st.session_state["messages"].append({"sender": "bot", "message": response.get("text", "Je n'ai pas compris votre question.")})

# L'application se rafraîchit automatiquement après chaque interaction avec le formulaire
