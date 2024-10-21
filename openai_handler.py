import os
from openai import OpenAI
import json
import time

class OpenAIHandler:
    def __init__(self):
        try:
            self.openai_api_key = os.getenv('ANKI_OPENAI_API_KEY')
            self.client = OpenAI(api_key=self.openai_api_key)
            self.assistant_id = "asst_MYeN7hvrv9jd2DJKorZP1Gkk"
        except Exception as e:
            print(f"Error initializing OpenAI client: {e}. If you have not set the ANKI_OPENAI_API_KEY environment variable, please set it and try again.")
            raise e

    def get_openai_response(self, hanzi):
        print("Getting OpenAI response for hanzi:", hanzi)

        thread = self.client.beta.threads.create()
        message = self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=f"Provide example data for: {hanzi}"
        )

        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=self.assistant_id,
        )

        if run.status == 'completed':
            messages = self.client.beta.threads.messages.list(
                thread_id=thread.id
            )
            print(messages)
        else:
            print(run.status)

        tool_outputs = []

        for tool in run.required_action.submit_tool_outputs.tool_calls:
            if tool.function.name == 'provide_example_sentence':
                tool_outputs.append({
                    "tool_call_id": tool.id,
                    "output": "tool output"
                })

        if tool_outputs:
            try: 
                run = self.client.beta.threads.runs.submit_tool_outputs_and_poll(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
                print("tool outputs submitted")
            except Exception as e:
                print(f"Error submitting tool outputs: {e}")
                raise e
        else:
            print("no tool outputs to submit")

        if run.status == 'completed':
            messages = self.client.beta.threads.messages.list(
                thread_id=thread.id
            )
            print(messages)
        else:
            print(run.status)   

        try:
            print("Here is the response:", messages[-1].content[0].text.value)
            # response_dict = json.loads(messages[-1].content[0].text.value)
            # return {
            #     'sentence': response_dict['example_sentence'],
            #     'translations': response_dict['english_translation'],
            #     'pinyin': response_dict['pinyin']
            # }
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from assistant response: {e}")
            raise e
        except KeyError as e:
            print(f"Missing expected key in assistant response: {e}")
            raise e
        except Exception as e:
            print(f"Unexpected error processing assistant response: {e}")
            raise e


