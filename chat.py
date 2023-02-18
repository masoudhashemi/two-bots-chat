import os

import openai
import streamlit as st

from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


def generate(prompt):
    model = "text-davinci-003"
    params = {
        "temperature": 0.2,
        "max_tokens": 250,
        "top_p": 0.98,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "stop": ["Chatbot1:", "Chatbot2:"],
    }
    # Call the OpenAI API to generate the sentence
    response = openai.Completion.create(engine=model, prompt=prompt, **params)

    # Return the generated sentence
    sentence = response.choices[0].text.strip()
    return sentence


# Set the page title
st.set_page_config(page_title="Chat App")

# Add a title to the page
st.title("Chat App")

# Function to reset the chat history
def reset_chat_history():
    st.session_state.chat_history = [("Rule", "There are two Chatbots (Chatbot1, Chatbot2) talking to each other.")]
    st.session_state.prev_bot1_input = ""
    st.session_state.prev_bot2_input = ""


# Create an empty list to store messages
if "chat_history" not in st.session_state:
    reset_chat_history()

# Create two input text boxes for users to enter their messages
bot1_input = st.text_area("Rule for Chatbot1:", key="bot1_input", value=st.session_state.prev_bot1_input)
bot2_input = st.text_area("Rule for Chatbot2:", key="bot2_input", value=st.session_state.prev_bot2_input)

# Remove earlier entries if the total length of all messages is greater than 2000 characters
# Do not remove the rules
while sum([len(message) for sender, message in st.session_state.chat_history]) > 2000:
    if "Rule" not in st.session_state.chat_history[0]:
        st.session_state.chat_history.pop(0)

# Create two columns to display the user input and bot response
col1, col2, col3 = st.columns(3)

# Create a button to submit the message
with col1:
    if st.button("Send"):
        # Add the user's message to the chat history
        bot1_changed = bot1_input != st.session_state.prev_bot1_input
        if bot1_changed:
            bot1_changed = True
            st.session_state.chat_history.append(("Rule for Chatbot1", bot1_input))
            st.session_state.prev_bot1_input = bot1_input

        # Generate a response from the Chatbot1
        prompt = "".join(
            [
                f"{sender}: {message}\n"
                for sender, message in st.session_state.chat_history
                if "Rule for Chatbot2" not in sender
            ]
        )
        bot1_response = generate(prompt + "\nChatbot1: ")

        # Add the bot1's response to the chat history
        st.session_state.chat_history.append(("Chatbot1", bot1_response))

        # Add the user's message to the chat history
        bot2_changed = bot2_input != st.session_state.prev_bot2_input
        if bot2_changed:
            bot2_changed = True
            st.session_state.chat_history.append(("Rule for Chatbot2", bot2_input))
            st.session_state.prev_bot2_input = bot2_input

        # Generate a response from the Chatbot2
        prompt = "".join(
            [
                f"{sender}: {message}\n"
                for sender, message in st.session_state.chat_history
                if "Rule for Chatbot1" not in sender
            ]
        )
        bot2_response = generate(prompt + "\nChatbot2: ")

        # Add the bot2's response to the chat history
        st.session_state.chat_history.append(("Chatbot2", bot2_response))


# Clear the history if the user clicks the button
with col2:
    if st.button("Clear History"):
        reset_chat_history()

# Clear the history if the user clicks the button
with col3:
    if st.button("Remove Last Entry"):
        if "Rule" not in st.session_state.chat_history[-1][0]:
            st.session_state.chat_history.pop(-1)

# Display the chat history
st.markdown("### Chat History")

for sender, message in st.session_state.chat_history:
    if "Rule" in sender:
        css_class = "rules"
    elif sender == "Chatbot1":
        css_class = "chatbot1"
    else:
        css_class = "chatbot2"

    with st.container():
        st.markdown(f"<div class='{css_class}'><b>{sender}:</b> {message}</div>", unsafe_allow_html=True)

# Define CSS styles for chatbot1 and chatbot2
st.markdown(
    """
    <style>
    .chatbot1 {
        background-color: #E0E0E0;
        padding: 5px;
        border-radius: 5px;
    }
    .chatbot2 {
        background-color: white;
        padding: 5px;
        border-radius: 5px;
    }
    .rules {
        background-color: #8FBC8F;
        padding: 5px;
        border-radius: 5px;
    }
    </style>
""",
    unsafe_allow_html=True,
)
