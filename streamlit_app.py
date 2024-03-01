import streamlit as st
from openai import OpenAI
from llm import full_response

st.title("AskCole v4")
st.markdown("This is AskCole. You can ask questions about how to (1) start a sales call, (2) transitioning to pitching, (3) pitching, (4) closing, and (5) handling objections.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hey there! How can I help you level up your sales game today?"}]

if "llm_messages" not in st.session_state:
    st.session_state.llm_messages = [{"role": "assistant", "content": "Hey there! How can I help you level up your sales game today?"}]

if st.session_state.get("started", False) == True:
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("How can I help?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.llm_messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.llm_messages
                ]
            stream = full_response(messages)
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.llm_messages.append({"role": "assistant", "content": response})
        st.rerun()

if st.sidebar.button("Start/Restart"):
    #clear the entire session state
    st.session_state.clear()
    st.session_state['started'] = True
    #rerun
    st.rerun()
    
if not st.session_state.get('category'):
    st.session_state.category = ""

if not st.session_state.get("previous_category"):
    st.session_state.previous_category = ""

st.sidebar.text_area("Category", value = st.session_state.category)

if not st.session_state.get('chunks'):
    st.session_state.chunks = ""

st.sidebar.text_area("Chunks", value = st.session_state.chunks)
