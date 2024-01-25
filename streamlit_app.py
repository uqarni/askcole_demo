from aifuncs import initialize_all_vdbs, generate_cole_response
from openai import OpenAI
import streamlit as st
import os

if st.session_state.get("dbs") is None:
    st.session_state["dbs"] = initialize_all_vdbs()

st.title("AskCole")

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
        dbs = st.session_state.dbs
        for response in generate_cole_response(st.session_state.messages, dbs, st.session_state):
            full_response += (response or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})


st.sidebar.title("Response Variables")
#show the session_state variables: topic, answer_prompt, examples, original_outgoig, colified_outgoing with a title above each one
st.sidebar.subheader("Topic")
st.sidebar.write(st.session_state.get("topic", ""))
# st.sidebar.write("Answer Prompt")
# st.sidebar.write(st.session_state.get("answer_prompt", ""))
st.sidebar.subheader("Examples")
st.sidebar.write(st.session_state.get("examples", ""))
st.sidebar.subheader("Summary")
st.sidebar.write(st.session_state.get("summary", ""))
#button to reset session_state
if st.sidebar.button("Reset Session State"):
    st.session_state = {}
