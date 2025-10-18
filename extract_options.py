import ast
import json

def add_specific_animal(animal):
    classification = animal["classification"]
    for i in range(len(classification)):
        newset.add(classification[i][1])

newset = set()
with open(f"data/{"list"}.json", "r", encoding="utf8") as list_file:
    animal_list = ast.literal_eval(list_file.read())
    n_animals = len(animal_list)
for i in range(n_animals):
    newset.add(animal_list[i])
    with open(f"data/{animal_list[i]}.json", "r", encoding="utf8") as animal_file:
        add_specific_animal(ast.literal_eval(animal_file.read()))

with open(f"data/{"auto_complet_option"}.json", "w", encoding="utf8") as auto_complet_option:
    auto_complet_option.write(json.dumps(sorted(list(newset))))
