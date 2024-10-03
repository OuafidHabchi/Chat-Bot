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
        return response.json()  # Try to parse the response to JSON
    except requests.exceptions.Timeout:
        return [{"text": "Le serveur a mis trop de temps à répondre. Réessayez plus tard."}]
    except requests.exceptions.ConnectionError:
        return [{"text": "Impossible de se connecter au serveur Rasa. Assurez-vous qu'il est bien démarré."}]
    except requests.exceptions.RequestException as e:
        return [{"text": f"Une erreur HTTP s'est produite : {e}"}]
    except ValueError:
        return [{"text": "La réponse du serveur n'était pas au format JSON."}]

# Function to display the exchanged messages
def display_messages():
    for message in st.session_state["messages"]:
        if message["sender"] == "user":
            st.markdown(f'<div class="user-bubble">{message["message"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-bubble">{message["message"]}</div>', unsafe_allow_html=True)

# Call the function to display messages
display_messages()

# Using `st.form` for user input
with st.form(key="user_input_form", clear_on_submit=True):
    user_message = st.text_input("Tapez votre message ici...")
    submit_button = st.form_submit_button("Envoyer")

# If the user submits a message
if submit_button and user_message:
    # Add the user's message to the message history immediately
    st.session_state["messages"].append({"sender": "user", "message": user_message})
    
    # Refresh UI to display the user's message before processing the bot's response
    display_messages()
    st.experimental_rerun()

# Show a spinner to simulate the chatbot "thinking" (if messages were just added)
if len(st.session_state["messages"]) > 0 and st.session_state["messages"][-1]["sender"] == "user":
    with st.spinner("Le chatbot est en train de réfléchir..."):
        # Send the message to Rasa and get the response
        user_message = st.session_state["messages"][-1]["message"]
        responses = send_message_to_rasa(user_message)

        # After getting the response, append the bot's response to the history
        if responses:  # Check if any responses were received
            for response in responses:
                if 'text' in response:
                    st.session_state["messages"].append({"sender": "bot", "message": response["text"]})
                else:
                    st.session_state["messages"].append({"sender": "bot", "message": "Je n'ai pas compris votre question."})

        # Trigger an immediate rerun to display bot's message
        st.experimental_rerun()
