import os
import json

class TypingAssistant:
    
    def __init__(self):
        try:
            with open(".model.json", "r", encoding="utf-8") as model_json:
                self.data_model = json.load(model_json)
        except FileNotFoundError:
            self.data_model = {"Typing Assistant": {}}
            self.update_json()

    def update_json(self):
        with open("model.json", "w", encoding="utf-8") as model_json:
            json.dump(self.data_model, model_json, indent=4)

    def add_line(self, line, assistant="Typing Assistant"):
        if assistant != "Typing Assistant":
            self.add_line(line, "Typing Assistant")
        comes_from = ""
        line = line.split()
        for symbol in line:
            if assistant in self.data_model:
                if comes_from in self.data_model[assistant]:
                    if symbol in self.data_model[assistant][comes_from]:
                        self.data_model[assistant][comes_from][symbol] += 1
                    else:
                        self.data_model[assistant][comes_from][symbol] = 1
                else:
                    self.data_model[assistant][comes_from] = {symbol: 1}
            else:
                self.data_model[assistant] = {comes_from: {symbol: 1}}
            comes_from = symbol
    
    def add_text(self, text_name, assistant="Typing Assistant"):
        with open(text_name, "r", encoding="utf-8") as file:
            lines = file.readlines()
        for line in lines:
            self.add_line(line, assistant)
        self.update_json()

    def add_folder(self, folder_name):
        directory = os.listdir(f"{os.getcwd()}/{folder_name}")
        for file_name in directory:
            file_path = f"{folder_name}/{file_name}"
            if file_name.endswith(".txt"):
                self.add_text(file_path, folder_name.split("/")[-1])
            elif "." not in file_name:
                self.add_folder(file_path)

typing_assistant = TypingAssistant()
typing_assistant.add_folder("data")