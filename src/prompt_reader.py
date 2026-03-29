import os
import json

class PromptReader:
    def __init__(self, prompt_file: str):
        file = open(prompt_file, "r")
        self.prompts = json.load(file)

    def get_prompt(self, role: str) -> str:
        return self.prompts[role]['prompt']

    def get_type(self, role: str) -> str:
        return self.prompts[role]['type']