import os
import json

class TypingAssistant:
    
    def __init__(self):
        try:
            with open(".model.json", "r", encoding="utf-8") as model_json:
                self.data_model = json.load(model_json)
        except FileNotFoundError:
            self.data_model = {"Typing Assistant": {}}
    
    def __str__(self):
        return json.dumps(self.data_model, ensure_ascii=False, indent=4)

    def add_line(self, line, assistant="Typing Assistant"):
        if assistant != "Typing Assistant":
            if assistant not in self.data_model:
                self.data_model[assistant] = {}
            self.add_line(line, "Typing Assistant")
        last_path = self.data_model[assistant]
        line = line.split()
        for symbol in line:
            if symbol in last_path:
                last_path[symbol][""] += 1
            else:
                last_path[symbol] = {"": 1}
            last_path = last_path[symbol]
    
    def add_text(self, text_name, assistant="Typing Assistant"):
        with open(text_name, "r", encoding="utf-8") as file:
            lines = file.readlines()
        for line in lines:
            sublines = line.split(".")
            for subline in sublines:
                self.add_line(subline, assistant)

    def add_folder(self, folder_name):
        directory = os.listdir(f"{os.getcwd()}/{folder_name}")
        for file_name in directory:
            file_path = f"{folder_name}/{file_name}"
            if file_name.endswith(".txt"):
                self.add_text(file_path, folder_name.split("/")[-1])
            elif "." not in file_name:
                self.add_folder(file_path)

    def next(self, line, assistant="Typing Assistant"):
        next_symbols = {}
        if assistant in self.data_model:
            line = line.split()
            trees = TypingAssistant.__all_trees(self.data_model[assistant], line[0])
            for tree in trees:
                for symbol in line:
                    if symbol in tree:
                        tree = tree[symbol]
                    else:
                        tree = {}
                for symbol in tree:
                    if symbol:
                        if symbol in next_symbols:
                            next_symbols[symbol] += tree[symbol][""]
                        else:
                            next_symbols[symbol] = tree[symbol][""]
            total = sum(next_symbols.values())
            for symbol in next_symbols:
                next_symbols[symbol] = round(next_symbols[symbol] / total, 2)
        return sorted(next_symbols.items(), key=lambda symbol: symbol[1], reverse=True)
    
    def save(self):
        with open(".model.json", "w", encoding="utf-8") as model_json:
            json.dump(self.data_model, model_json, ensure_ascii=False)

    def empty(self):
        self.data_model = {}
        self.save()

    @staticmethod
    def __all_trees(tree, root):
        if root in tree:
            trees = [tree]
        else:
            trees = []
        for symbol in tree:
            if isinstance(tree[symbol], dict):
                trees.extend(TypingAssistant.__all_trees(tree[symbol], root))
        return trees

typing_assistant = TypingAssistant()