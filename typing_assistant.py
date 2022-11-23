import os
import json
import shutil

class TypingAssistant:

    def __init__(self):
        self.model_path = os.path.join(os.getcwd(), "model")

    def next(self, line, assistant="Typing Assistant"):
        next_symbols = {}
        line = line.split()
        for i in range(len(line)-1):
            subline = line[i:]
            next_symbols[" ".join(subline)] = self.__last_leaf(subline, assistant)
        return next_symbols
    
    def add_line(self, line, assistant="Typing Assistant"):
        if len(line) >= 2:
            if assistant != "Typing Assistant":
                self.add_line(line, "Typing Assistant")
            root = line[0]
            model_path = os.path.join(self.model_path, assistant, f"{root}.json")
            if self.__path_exits(assistant, f"{root}.json"):
                with open(model_path, "r", encoding="utf-8") as model_json:
                    tree = json.load(model_json)
            else:
                if not self.__path_exits(assistant):
                    os.makedirs(os.path.join(self.model_path, assistant))
                tree = {}
            last_tree = tree
            subline = line[1:]
            for symbol in subline:
                if symbol in last_tree:
                    last_tree[symbol][""] += 1
                else:
                    last_tree[symbol] = {"": 1}
                last_tree = last_tree[symbol]
            with open(model_path, "w", encoding="utf-8") as model_json:
                json.dump(tree, model_json, ensure_ascii=False)
            return self.add_line(line[1:], assistant)
    
    def add_text(self, text_name, assistant="Typing Assistant"):
        print(f"    {text_name}")
        with open(text_name, "r", encoding="utf-8") as file:
            lines = file.readlines()
        for line in lines:
            sublines = line.split(".")
            for subline in sublines:
                self.add_line(subline.split(), assistant)
    
    def add_folder(self, folder_name):
        directory = sorted(os.listdir(os.path.join(os.getcwd(), folder_name)))
        for file_name in directory:
            file_path = os.path.join(folder_name, file_name)
            if os.path.isfile(file_path):
                self.add_text(file_path, "Typing Assistant")
            elif os.path.isdir(file_path):
                self.add_folder(file_path)

    def empty(self):
        if self.__path_exits():
            shutil.rmtree(self.model_path)
    
    def __path_exits(self, *paths):
        path = os.path.join(self.model_path, *paths)
        return os.path.exists(path)
    
    def __last_leaf(self, line, assistant="Typing Assistant"):
        root = line[0]
        if self.__path_exits(assistant, f"{root}.json"):
            model_path = os.path.join(self.model_path, assistant, f"{root}.json")
            with open(model_path, "r", encoding="utf-8") as model_json:
                tree = json.load(model_json)
            for symbol in line[1:]:
                if symbol in tree:
                    tree = tree[symbol]
                else:
                    return {}
            del tree[""]
            for symbol in tree:
                tree[symbol] = tree[symbol][""]
            return tree
        return {}
