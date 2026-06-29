from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
load_dotenv()

from tools.ec2_tool import(
 create_ec2_instance,
    list_instances,
    start_instance,
    stop_instance,
    terminate_instance
)



system_prompt = """
You are an AWS EC2 assistant.

Rules:
1. Only call the tool explicitly required by the user.
2. Never stop, terminate, or start an instance unless the user explicitly requests it.
3. After creating an EC2 instance, return the result and stop.
4. Do not perform additional actions automatically.
"""

# llm = ChatGroq(
#     model="llama-3.3-70b-versatile",
#     temperature=0
# )
llm = ChatOllama(
    model="llama3.1:latest",
    temperature=0
)

tools = [
    create_ec2_instance,
    list_instances,
    start_instance,
    stop_instance,
    terminate_instance
    ]

agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=system_prompt,
    debug=True
)
