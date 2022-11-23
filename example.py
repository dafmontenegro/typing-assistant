from typing_assistant import TypingAssistant

def read_file(text_name):
    with open(text_name, "r", encoding="utf-8") as file:
        file_lines = file.readlines()
    return [file_line.split(".") for file_line in file_lines]

n_lines = 0
average_accuracy = 0
lines = read_file("test.txt")
typing_assistant = TypingAssistant()
for line in lines:
    for subline in line:
        subline = subline.split()
        if len(subline) >= 2:
            successes = 0
            for i in range(2, len(subline)):
                next_symbols = typing_assistant.next(" ".join(subline[:i]), "Julio Cortázar")
                if subline[i] in next_symbols:
                    successes += 1
            print(" ".join(subline), round(successes/(len(subline)-2), 4))
            average_accuracy += round(successes/(len(subline)-2), 4)
            n_lines += 1
print("AVERAGE:", round(average_accuracy/n_lines, 4))