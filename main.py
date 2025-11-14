from agent import CalendarAgent

if __name__ == "__main__":
    agent = CalendarAgent()

    prompt = "Help me put a calendar event in my diary."

    while True:
        result = agent.run_agent(prompt)
        print("Agent:", result)

        if result.startswith("Event created"):
            break
        prompt = input("User: ")
