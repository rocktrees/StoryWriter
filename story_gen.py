from tqdm import tqdm
import json
import fire
from openai import OpenAI

SYSTEM_PROMPT_BASE: str = '''
    I have bullet point summaries of a hidden story. You are a creative genius, famous for writing amazing novels. \
    Uncover the hidden story from these points. You will only be given one point at a time, and the result of each\
        subsequent point will be influenced by the previous generation. STRICTLY use ONLY 133 to 200 tokens per generation; DO NOT generate significantly fewer or greater than this.
    Be careful so that each generation sticks only to the given summary point.
    The generated story chucks should hint at the points, not out right say it. So carefully use words that envelop the point without copying words from it.
    Make sure the new generated plot connects seamless with the previous one.
    Everytime the story starts, use the tag "[START]" '''

ADDITION: str = '''
        For this story, there is a specfic setting, genre, style of prose, and characters.
        Setting: {}
        Genre: {}
        style of prose: {}
        characters: {}

        For characters, they will always be given in this format
            EX) name: description
        
        ONLY use the character information IF you run across a character in the summary points that has the same name. Otherwise, disregard them.

        Finally, have fun with the details given! Write a captivating story that is exciting to read using these additional information.
        '''


class StoryGen:
    '''This class gives easy access to the story generator. It is model agnostic and easy to tweak.
    '''

    #TODO Need to move the model name into main. Command line argument
    def __init__(self, key: str, params: dict, model_name: str = "anthropic/claude-2"):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=key,
        )
        self.params = params
        self.model_name = model_name
        self.chat_history = []

    def response(self):
        '''main text generation happens here!
        I ran into issues with the api at this point, so it will try up to 3 times 
        when it runs into pre-defined errors. After i set this try except block, I stopped having issues.
        '''
        for _ in range(3):
            try:
                completion = self.client.chat.completions.create(model=self.model_name,
                                                                 messages=self.chat_history,
                                                                 temperature=.5)
                return completion.choices[0].message.content
            except (TypeError, json.JSONDecodeError):
                pass  # try again
        return "Failed to generate after 3 retries"

    def generate(self, user_input):
        '''Generates the specfic prompt neccesary for proper generation
        '''
        if len(self.chat_history) == 0:
            self.chat_history.append(
                {"role": "system", "content": SYSTEM_PROMPT_BASE})

            '''If param exists on the first run, then apply the modification.
            '''
            if len(self.params) > 0:
                self.chat_history.append(
                    {"role": "user", "content": ADDITION.format(self.params['setting'],
                                                                self.params['genre'],
                                                                self.params['style of prose'],
                                                                self.params['characters_info'])})

        self.chat_history.append({"role": "user", "content": user_input})

        repsonse_formatted = {"role": "assistant", "content": self.response()}
        self.chat_history.append(repsonse_formatted)
        return repsonse_formatted

    def save_chat_history(self, filename: str):
        with open(filename, 'w') as f:
            json.dump(self.chat_history, f)


def verify_params(parameters: bool):
    '''Handles inputs
    '''
    if parameters:
        # list of characters
        parameters_info = {"characters_info": [],
                           "setting": "",
                           "genre": "",
                           "style of prose": ""}

        print("Give the name of a character and some details about them like this.\
                              \nEx) Justin: Kind hearted, bald headed man\
                              \ntype 'done' when you're finished!\n")
        while True:
            temp_info = input("Character info: ")
            if temp_info.lower().strip() == "done":
                break
            parameters_info['characters_info'].append(temp_info)

        parameters_info['setting'] = input("What is the setting?: ")
        parameters_info['genre'] = input("What is the genre?: ")
        parameters_info['style of prose'] = input(
            "What is the style of prose?: ")

    else:
        parameters_info = {}

    return parameters_info


def main(key: str = "",
         parameters: bool = False):
    '''Engine of the program
    '''

    # first, pull the points
    with open("points.json", "r") as stream:
        points_data = json.load(stream)

    parameters_info = verify_params(parameters)

    story_generator = StoryGen(key=key, params=parameters_info)

    for point in tqdm(points_data['points']):

        response = story_generator.generate(point)

        '''Sometimes the '[START]' is not generated, so we have to maneuver around that
        '''
        if '[START]' in response['content']:
            story = response['content'].split('[START]')[1]
        else:
            story = response['content']
        print(f"{story}\n---")

    story_generator.save_chat_history("chat_history.json")


if __name__ == "__main__":
    fire.Fire(main)
