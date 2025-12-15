from agent import CalendarAgent

if __name__ == "__main__":
    agent = CalendarAgent("gpt-5-nano")

    prompt = ""

    while True:
        result = agent.run_agent(prompt)
        print("Agent:", result)

        prompt = input("User: ")
