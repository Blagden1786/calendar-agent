import json
from openai import OpenAI

from datetime import datetime
from tools.create_event_tool import create_event, create_event_function
from tools.delete_event_tool import delete_event, delete_event_function
from tools.edit_event_tool import edit_event, edit_event_function
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

4. You can update events in their calendar.
You must first call the list_events tool to find the event ID of the event to update
Once you have found the event, ask the user to confirm this is the correct one.
Call the edit_event tool with the eventID and new details.


The current date is {str(datetime.today()).split()[0]}

When giving the details as instructed by the tool, make sure to correctly capitalise the event name.

On the first respose you give, briefly explain your role and what you can do. Do not give any details about your process, just the four things you can do.
Once you have used the necessary tools, call no tools and return a text response."""

class CalendarAgent:
    def __init__(self, model="gpt-5-nano"):
        self.agent = OpenAI()
        self.model = model
        self.tools = [create_event_function, list_events_function, delete_event_function, edit_event_function]

        self.prompt = PROMPT
        self.inputs = []

    def get_response(self):
        response = self.agent.responses.create(model=self.model, tools=self.tools, input=self.inputs, instructions=self.prompt)
        return response

    def run_agent(self, prompt=""):

        while True:
            tool_used = False
            # Append user prompt to input list
            self.inputs += [{'role': 'user', 'content': prompt}]

            # Get response from the agent
            response = self.get_response()

            # Add output of agent to inputs
            self.inputs += response.output

            for item in response.output:
                # Check for a function call - if there is, need to call the corresponding function
                if item.type == 'function_call':
                    tool_used = True
                    print(f"Function to call: {item.name}")
                    print(f"Arguments: {item.arguments}")

                    # When more tools are added, use a switch statment or a mapping to
                    # Call the corresponding function
                    result = globals()[item.name](**json.loads(item.arguments))
                    #print(f"Function result: {result}")

                    # Append the function call and result to the conversation
                    self.inputs.append({
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": json.dumps({
                        f"{item.name}": result
                        })
                    })

            if not tool_used:
                return response.output_text
