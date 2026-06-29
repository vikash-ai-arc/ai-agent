import streamlit as st
from agent.ec2_agent import agent
from langchain_core.messages import HumanMessage

st.title("AWS AI Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

prompt = st.chat_input(
    "Ask your AWS agent..."
)

if prompt:
    st.session_state.messages.append(
        ("user", prompt)
    )

    response = agent.invoke(
        {
            "messages": [
                HumanMessage(content=prompt)
            ]
        }
    )

    answer = response["messages"][-1].content

    st.session_state.messages.append(
        ("assistant", answer)
    )

for role, msg in st.session_state.messages:
    with st.chat_message(role):
        st.write(msg)