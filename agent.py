from google import genai
from google.genai import types

from tools.create_event_tool import *


PROMPT = """You are a calendar assistant. You can help users create calendar events and answer questions. Use the tools available to you to assist the user. If you need more information, use the ask_question tool to get the necessary details before creating an event.

Current conversation:"""

class CalendarAgent:
    def __init__(self, model="gemini-2.5-flash"):
        self.agent = genai.Client()
        self.tools = types.Tool(function_declarations=[create_event_function])
        self.config = types.GenerateContentConfig(tools=[self.tools])

        self.prompt = PROMPT

    def get_response(self, prompt):
        response = self.agent.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=self.config,
        )
        return response

    def run_agent(self, prompt):
        response = self.get_response(self.prompt + "\nUser: " + prompt)

        # Check for a function call
        if response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call
            print(f"Function to call: {function_call.name}")
            print(f"Arguments: {function_call.args}")

            # When more tools are added, use a switch statment or a mapping to
            # Call the corresponding function
            result = globals()[function_call.name](**function_call.args)
            return result
        else:
            print("No function call found in the response.")

            self.prompt += f"\nUser: {prompt}\nAssistant: {response.text}"
            return response.text
