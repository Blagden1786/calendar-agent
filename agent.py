from google import genai
from google.genai import types

import datetime
from tools.create_event_tool import create_event, create_event_function
from tools.delete_event_tool import delete_event, delete_event_function
from tools.list_events_tool import list_events, list_events_function


PROMPT = f"""You are a calendar assistant. You can help users with their calendar. You currently have the following abilities:

1. You can answer simple questions about their calendar.

2. You can create events in their calendar by asking them the necessary information:
In order to find out the event, ask one question at a time to the user, they will respond and then you can ask the next question.
You should gain the following necessary info:
Event name:
Start time and date:
End time and date:
Location: (optional)
Description: (optional)

3. You can delete events from their calendar.
You must first call the list_events tool to find the event ID of the event to delete.
Once you have found the event to delete, ask the user to confirm they want to delete the event.
You can then call the delete_event tool with the event ID to delete the event.

The current date is {str(datetime.datetime.today()).split()[0]}

When giving the details as instructed by the tool, make sure to correctly capitalise the event name.

On the first respose you give, briefly explain your role and what you can do.
Current conversation:"""

class CalendarAgent:
    def __init__(self, model="gemini-2.5-flash"):
        self.agent = genai.Client()
        self.tools = types.Tool(function_declarations=[create_event_function, list_events_function, delete_event_function])
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
        while True:
            # Append user prompt to conversation
            if prompt:
                self.prompt += f"\nUser: {prompt}\n"

            # Get response from the agent
            response = self.get_response(self.prompt)

            # Check for a function call - if there is, need to call the corresponding function
            if response.candidates[0].content.parts[0].function_call:
                function_call = response.candidates[0].content.parts[0].function_call
                print(f"Function to call: {function_call.name}")
                print(f"Arguments: {function_call.args}")

                # When more tools are added, use a switch statment or a mapping to
                # Call the corresponding function
                result = globals()[function_call.name](**function_call.args)
                #print(f"Function result: {result}")

                # Append the function call and result to the conversation
                self.prompt += f"Assistant: {response}\nFunction {function_call.name} called with arguments {function_call.args} and returned {result}\n"

                # Some tool calls may finish the task - in this case return the result
                if function_call.name != "list_events":
                    return result

            else:
                #print("No function call found in the response.")

                self.prompt += f"\nUser: {prompt}\nAssistant: {response.text}"
                return response.text
