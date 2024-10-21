import os
from openai import OpenAI

class OpenAIHandler:
    def __init__(self):
        try:
            self.openai_api_key = os.getenv('ANKI_OPENAI_API_KEY')
            self.client = OpenAI(api_key=self.openai_api_key)
        except Exception as e:
            print(f"Error initializing OpenAI client: {e}. If you have not set the ANKI_OPENAI_API_KEY environment variable, please set it and try again.")
            raise e

    def get_openai_response(self, hanzi):
        # Return a dictionary with the following keys: sentence, translation, pinyin

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "you are a helpful Chinese learning assistant that takes one or more hanzi characters and returns a comma delimited list of the following and nothing else: 1. example sentence using those characters 2. the english translation of that sentence 3. the pinyin of that sentence. For example, if the input is '钥匙' the output could be '我把钥匙丢在办公室里了, I left my keys in the office, wǒ bǎ yào shi diào zài gōng shì lǐ le,'", "role": "user", "content": hanzi}]
        )

        # Split the response into a list of strings
        response_list = response.choices[0].message.content.split(',')

        try:
            return {
                'sentence': response_list[0],
                'translations': response_list[1],
                'pinyin': response_list[2]
            }
        except Exception as e:
            print(f"OpenAI response is not in the expected format: {e}")
            raise e

