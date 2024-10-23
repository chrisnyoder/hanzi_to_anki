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
        thread = self.create_thread()
        run = self.create_and_poll_run(thread.id, hanzi)
        tool_outputs = self.handle_tool_outputs(run)
        run = self.wait_for_completion(run, thread.id, tool_outputs)
        return self.process_response(thread.id, hanzi)

    def create_thread(self):
        return self.client.beta.threads.create()

    def create_and_poll_run(self, thread_id, hanzi):
        self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=f"Provide example sentences for {hanzi} in JSON format"
        )

        return self.client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=self.assistant_id,
        )

    def handle_tool_outputs(self, run):
        tool_outputs = []
        for tool in run.required_action.submit_tool_outputs.tool_calls:
            if tool.function.name == 'provide_example_sentence':
                tool_outputs.append({
                    "tool_call_id": tool.id,  # Ensure this ID matches the expected call ID
                    "output": json.dumps({"success": True})  # Correct JSON format
                })
        return tool_outputs

    def wait_for_completion(self, run, thread_id, tool_outputs):    
        run = self.submit_tool_outputs(run, tool_outputs, thread_id)
        time.sleep(1)
        timer = 0
        
        while run.status != 'completed':
            if run.status == 'requires_action':                
                run = self.client.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run.id
                )

                if run.required_action and run.required_action.submit_tool_outputs:
                    tool_outputs = self.handle_tool_outputs(run)
                    if tool_outputs:
                        run = self.submit_tool_outputs(run, tool_outputs, thread_id)

            time.sleep(1)
            timer += 1
            if timer > 10:
                print("run status still not completed after 10 seconds")
                raise Exception("Run status not completed after 10 seconds")
        return run
    
    def submit_tool_outputs(self, run, tool_outputs, thread_id):
        if tool_outputs:
            try:
                return self.client.beta.threads.runs.submit_tool_outputs_and_poll(
                    thread_id=thread_id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
            except Exception as e:
                print(f"Error submitting tool outputs: {e}")
                raise e
        else:
            print("no tool outputs to submit")

    def process_response(self, thread_id, hanzi):
        messages = self.client.beta.threads.messages.list(thread_id=thread_id)
        try:
            response_dict = json.loads(messages.data[0].content[0].text.value)

            return {
                'hanzi': hanzi,
                'example_sentence': response_dict['example_sentence'],
                'translations': [response_dict['english_translation']],
                'pinyin': response_dict['pinyin']
            }
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from assistant response: {e}")
            raise e
        except KeyError as e:
            print(f"Missing expected key in assistant response: {e}")
            raise e
        except Exception as e:
            print(f"Unexpected error processing assistant response: {e}")
            raise e



