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


instance_name = st.text_input("Instance Name")

instance_type = st.selectbox(
    "Instance Type",
    [
        "t3.micro",
        "t3.small",
        "t3.medium"
    ]
)

os_type = st.selectbox(
    "Operating System",
    [
        "Amazon Linux",
        "Ubuntu 24.04",
        "Ubuntu 22.04"
    ]
)

volume_size = st.number_input(
    "Volume Size",
    min_value=8,
    max_value=500,
    value=20
)