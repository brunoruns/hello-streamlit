from openai import OpenAI
import streamlit as st
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os


st.title("ChatBot tester")

client_mistral = MistralClient(api_key=os.environ["MISTRAL_API_KEY"])


if "mistral_model" not in st.session_state:
    st.session_state["mistral_model"] = "open-mistral-7b"

with st.sidebar:
    model_options = ('open-mistral-7b', 'open-mixtral-8x7b', 'open-mixtral-8x22b', 'mistral-tiny', 'mistral-small', 'mistral-medium', "mistral-large-latest")
    st.session_state["mistral_model"] = st.selectbox('Select a model', model_options, index=model_options.index(st.session_state["mistral_model"]), key="model_select")


if "messages" not in st.session_state:
    st.session_state.messages = []

#systeem prompt
if "system_prompt" not in st.session_state:
    st.session_state["system_prompt"] = """
    Je bent een informatica en AI specialist die advies geeft over coderen van modellen. Je geeft enkel advies over syntaxfouten, niet over fouten in logica van modellen. 
    """

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client_mistral.chat_stream(
            model=st.session_state["mistral_model"],
            messages=[ChatMessage(role = "system", content = st.session_state.system_prompt)] + [ChatMessage(role= m["role"], content = m["content"]) for m in st.session_state.messages])
        print(ChatMessage(role = "system", content = st.session_state.system_prompt))
        message_placeholder = st.empty()
        full_response = ""
        for response in stream:
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
