import json

rangsTaxonomiques = [
    "Domaine",
    "Règne",
    "Sous-règne",
    "Infra-règne",
    "Super-embr.",
    "Embranchement",
    "Sous-embr.",
    "Infra-embr.",
    "Super-classe",
    "Classe",
    "Sous-classe",
    "Infra-classe",
    "Cohorte",
    "Magnordre",
    "Super-ordre",
    "Ordre",
    "Sous-ordre",
    "Infra-ordre",
    "Micro-ordre",
    "Super-famille",
    "Famille",
    "Sous-famille",
    "Tribu",
    "Sous-tribu",
    "Genre",
    "Sous-genre",
    "Espèce",
    "Sous-espèce",
]

class Node:
    def __init__(self, rangTaxonomique, nom, parent):
        self.rangTaxonomique = rangTaxonomique
        self.nom = nom
        self.parent = parent
        self.descendants = set()
        if parent is not None:
            parent.descendants.add(self)
    
    def __str__(self):
        return f"{self.rangTaxonomique}: {self.nom}"


if __name__ == "__main__":
    eukariotes = Node("Domaine", "Eukaryota", None)
    animaux = Node("Règne", "Animalia", eukariotes)
    noeuds = {"Eukaryota": eukariotes, "Animalia": animaux}
    with open("data/list.json") as list_content:
        liste_des_animo  = json.load(list_content)
        for animal in liste_des_animo:
            with open(f"data/{animal}.json") as animal_content:
                classification = json.load(animal_content)["classification"]
                noeud = None
                for rangTaxonomique, taxon in classification:
                    if (taxon not in noeuds):
                        noeud = Node(rangTaxonomique, taxon, noeud)
                        noeuds[taxon] = noeud
                    else:
                        noeud = noeuds[taxon]
    
    noeud = eukariotes
    while True:
        print(noeud, "Revenir en arrière : z", sep="\n")
        listeDesDescendants = list(noeud.descendants)
        for k, d in enumerate(noeud.descendants):
            print(f"{k}: {d}")
        choice = input()
        if choice == "z" and noeud.parent is not None:
            noeud = noeud.parent
        elif choice.isdigit():
            choice = int(choice)
            if choice >= len(listeDesDescendants):
                print("Mauvais choix")
            else:
                noeud = listeDesDescendants[int(choice)]
        else:
            print("Mauvais choix")

                

