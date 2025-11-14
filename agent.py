from google import genai
from google.genai import types

from tools.create_event_tool import *


PROMPT = f"""You are a calendar assistant. You can help users create calendar events and answer questions. In order to find out the event, ask one question at a time to the user, they will respond and then you can ask the next question.
You should gain the following necessary info:
Event name:
Start time and date:
End time and date:

Additionally you should ask if they want to include a description or a location.
The current date is {str(datetime.datetime.today()).split()[0]}

When giving the details as instructed by the tool, make sure to correctly capitalise the event name.
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

    def run_agent(self, prompt=""):
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
