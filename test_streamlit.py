import openai
import streamlit as st
from streamlit_chat import message
import os

st.title("ChatGPT-like clone")

#openai.api_key = os.environ.get("API_KEY")
#password = os.environ.get("PASSWORD")
openai.api_key = "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"

#openai.api_key = st.secrets["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"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})