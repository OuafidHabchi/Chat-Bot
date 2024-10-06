import streamlit as st
import requests

# Rasa server URL
rasa_server_url = "http://54.87.201.152:5005/webhooks/rest/webhook"

# Title of the page
st.title("Assistant Virtuel - Chatbot")

# CSS for styling the chat bubbles
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
        clear: both.
    }
    </style>
""", unsafe_allow_html=True)

# Initialize the message history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Function to send a message to Rasa and get a response with timeout handling
def send_message_to_rasa(user_message, timeout=5):
    try:
        # Send the message to Rasa with a timeout
        response = requests.post(rasa_server_url, json={"sender": "user", "message": user_message}, timeout=timeout)
        response.raise_for_status()  # Check if the request was successful
        return response.json()  # Parse the response as JSON
    except requests.exceptions.Timeout:
        st.error("Le serveur a mis trop de temps à répondre. Veuillez réessayer.")
        return [{"text": "Le serveur Rasa a mis trop de temps à répondre, veuillez réessayer."}]
    except requests.exceptions.ConnectionError:
        st.error("Impossible de se connecter au serveur Rasa. Assurez-vous qu'il est bien démarré.")
        return [{"text": "Le serveur Rasa est injoignable, veuillez réessayer plus tard."}]
    except requests.exceptions.RequestException as e:
        st.error(f"Une erreur HTTP s'est produite : {e}")
        return [{"text": "Une erreur s'est produite lors de la connexion au serveur Rasa."}]
    except ValueError:
        st.error("La réponse du serveur n'était pas au format JSON.")
        return [{"text": "Je n'ai pas pu comprendre la réponse du serveur."}]

# Display the message history
for message in st.session_state["messages"]:
    if message["sender"] == "user":
        st.markdown(f'<div class="user-bubble">{message["message"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-bubble">{message["message"]}</div>', unsafe_allow_html=True)

# Using st.form for user message input
with st.form(key="user_input_form", clear_on_submit=True):
    user_message = st.text_input("Tapez votre message ici...")
    submit_button = st.form_submit_button("Envoyer")

# If the user submits a message
if submit_button and user_message:
    # Add the user message to the history
    st.session_state["messages"].append({"sender": "user", "message": user_message})

    # Send the message to Rasa and get the response
    responses = send_message_to_rasa(user_message)

    # Add the bot response to the history
    for response in responses:
        if 'text' in response:
            st.session_state["messages"].append({"sender": "bot", "message": response["text"]})
        else:
            st.session_state["messages"].append({"sender": "bot", "message": "Je n'ai pas compris votre question."})
