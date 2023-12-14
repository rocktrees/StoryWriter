# Story writer!

Author: Hyun Guk(Josh) Yoo

I've created a simple system that is able to take detailed story outlines, and create a complete, fluid story using LLMs!

I did this by leaning into prompt engineering. By outlining clear directions and framework, this software is able to take just a file of bullet points and stitch it together cohesively.

The way I decided to go about this was to feed the LLM one beat at a time. This way, the story is written one section at a time. This might allow the story to take a life on its own, and not have the beginning parts of the story be influenced by the later points.

# Features

I am using [OpenRouter](https://openrouter.ai/) which allows me to take advantage of OpenAI's api for almost any model. Just create a key with OpenRouter

It is able to take in these features to adjust the story to your liking.

1. Characters
2. Setting
3. Genre
4. Style of prose

# How to use

I've given you one story outline to play with, but please feel free to create your own! Your imagination is the limit, have fun!

An example output of the provided points is in **story_example.txt**

- Install python3.11 and python3.11-venv
- Create venv
  - `python3.11 -m venv .venv`
- Keep points in a json file called `points.json`
  - {
    "points": [
    "1. Begin with Jack...", "2. Jack ...
    ]
    }
- add openrouter key using this flag `--key`
  - `python3.11 story_gen.py --key <key here>`
- Note that the string `---` is used to notify that a new beat is being processed
- Run `story_gen.py` if you are not using any arguments
  - Full chat will be stored in `chat_history.json`
- If you are using arguments, use `parameters` flag
  - `python3.11 story_gen.py --parameters True`
  - You will be asked to input information about characters, setting, genre, and style of prose.
  - Designed to only use relavent information
