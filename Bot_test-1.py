import streamlit as st
import requests
import re  # Importer la bibliothèque pour utiliser les expressions régulières

# Définir l'URL du serveur Rasa
rasa_server_url = "http://138.197.172.64:5005/webhooks/rest/webhook"

# Titre de la page
st.title("Dispatch Virtuel ")

# Ajouter des liens vers les guides d'utilisation
st.markdown("""
### Guides d'utilisation
- [Guide d'utilisation en français](https://docs.google.com/document/d/1yaAk-Dn2gI6iAOqE6OtGBl351h0WAdDxhJq-TDY-rJ8/edit?usp=sharing)
- [User guide in English](https://docs.google.com/document/d/1Q-yKwCRPaHcGwcI0tj-jv6UOK7Ut53eQi0-0EBjg284/edit?usp=sharing)
""")

# CSS pour styliser les bulles de dialogue et rendre le conteneur défilable
st.markdown("""
    <style>
    .user-bubble {
        background-color: #A3E4D7;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        max-width: 60%;
        float: right;
        clear: both;
    }
    .bot-bubble {
        background-color: #85C1E9;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        max-width: 60%;
        float: left;
        clear: both;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        max-height: 400px;
        overflow-y: auto;
        border: 1px solid #ddd;
        padding: 10px;
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
        st.error("Impossible de se connecter au serveur Rasa. Assurez-vous qu'il est bien démarré.")
        return [{"text": "Le serveur Rasa est injoignable, veuillez réessayer plus tard."}]
    except requests.exceptions.RequestException as e:
        st.error(f"Une erreur HTTP s'est produite : {e}")
        return [{"text": "Une erreur s'est produite lors de la connexion au serveur Rasa."}]
    except ValueError:
        st.error("La réponse du serveur n'était pas au format JSON.")
        return [{"text": "Je n'ai pas pu comprendre la réponse du serveur."}]

# Fonction pour convertir les liens Markdown en HTML cliquable
def convert_markdown_links_to_html(text):
    # Expression régulière pour détecter les liens markdown de type [texte](url)
    markdown_link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    return re.sub(markdown_link_pattern, r'<a href="\2" target="_blank">\1</a>', text)

# Afficher les messages dans un conteneur défilable
chat_container = st.empty()  # Utiliser un conteneur vide pour les messages

with chat_container.container():  # Rafraîchir à chaque itération
    for message in st.session_state["messages"]:
        if message["sender"] == "user":
            st.markdown(f'<div class="user-bubble">{message["message"]}</div>', unsafe_allow_html=True)
        else:
            # Convertir les liens markdown en liens HTML cliquables
            bot_message_html = convert_markdown_links_to_html(message["message"])
            st.markdown(f'<div class="bot-bubble">{bot_message_html}</div>', unsafe_allow_html=True)

# Utilisation de `st.form` pour la saisie des messages utilisateur
with st.form(key="user_input_form", clear_on_submit=True):
    user_message = st.text_input("Tapez votre message ici...")
    submit_button = st.form_submit_button("Envoyer")

# Si l'utilisateur soumet un message
if submit_button and user_message:
    # Ajouter le message utilisateur à l'historique immédiatement
    st.session_state["messages"].append({"sender": "user", "message": user_message})

    # Envoyer le message à Rasa et obtenir la réponse
    responses = send_message_to_rasa(user_message)

    # Ajouter la réponse du bot à l'historique
    if responses:  # Vérifier si des réponses ont été reçues
        for response in responses:
            if 'text' in response:
                st.session_state["messages"].append({"sender": "bot", "message": response["text"]})
            else:
                st.session_state["messages"].append({"sender": "bot", "message": "Je n'ai pas compris votre question./ / I did not understand your question. Can you please repeat it ?"})
    else:
        st.session_state["messages"].append({"sender": "bot", "message": "Je n'ai pas compris votre question. Pouvez-vous la répéter SVP ? / I did not understand your question. Can you please repeat it ?"})

    # Forcer le conteneur de chat à scroller jusqu'au bas après l'ajout des messages
    with chat_container.container():
        for message in st.session_state["messages"]:
            if message["sender"] == "user":
                st.markdown(f'<div class="user-bubble">{message["message"]}</div>', unsafe_allow_html=True)
            else:
                # Convertir les liens markdown en liens HTML cliquables
                bot_message_html = convert_markdown_links_to_html(message["message"])
                st.markdown(f'<div class="bot-bubble">{bot_message_html}</div>', unsafe_allow_html=True)
