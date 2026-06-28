from agent.ec2_agent import agent

while True:
    user_input = input("\nEnter command (or 'exit'): ")

    if user_input.lower() == "exit":
        break

    response = agent.invoke(
        {
            "messages": [
                ("user", user_input)
            ]
        }
    )

    print("\nAgent Response:")
    print(response["messages"][-1].content)