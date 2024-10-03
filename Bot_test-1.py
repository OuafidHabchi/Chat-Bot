import streamlit as st
import requests

# Define the URL of your Rasa server
rasa_server_url = "http://3.87.73.156:5005/webhooks/rest/webhook"

# Title of the page
st.title("Assistant Virtuel - Chatbot")

# CSS to style the chat bubbles and position the discussion above the input field
st.markdown("""
    <style>
    .chat-container {
        display: flex;
        flex-direction: column-reverse;
        max-height: 500px;
        overflow-y: auto;
        padding-bottom: 20px;
    }
    .user-bubble {
        background-color: #DCF8C6;
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
        max-width: 60%;
        float: right;
        clear: both;
    }
    .bot-bubble {
        background-color: #F1F0F0;
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
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
        return [{"text": f"Une erreur s'est produite lors de la connexion : {e}"}]
    except ValueError:
        return [{"text": "La réponse du serveur n'était pas au format JSON."}]

# Function to display the exchanged messages
def display_messages():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for message in reversed(st.session_state["messages"]):  # Reverse the list so new messages appear at the bottom
        if message["sender"] == "user":
            st.markdown(f'<div class="user-bubble">{message["message"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-bubble">{message["message"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Call the function to display messages
display_messages()

# Using `st.form` for user input
with st.form(key="user_input_form", clear_on_submit=True):
    user_message = st.text_input("Tapez votre message ici...")
    submit_button = st.form_submit_button("Envoyer")

# If the user submits a message
if submit_button and user_message:
    # Show a spinner while waiting for the bot's response (Simulating the bot is thinking)
    with st.spinner("Le chatbot est en train de réfléchir..."):
        # Send the message to Rasa and get the response
        responses = send_message_to_rasa(user_message)

        # Append the user's message and the bot's response to the history
        st.session_state["messages"].append({"sender": "user", "message": user_message})

        # Append the bot's response or error message to the history
        if responses:
            for response in responses:
                st.session_state["messages"].append({"sender": "bot", "message": response["text"]})

    # Display both the user message and the bot's response together
    display_messages()
