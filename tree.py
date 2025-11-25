import json
import random

rangsTaxonomiques = [
    "Domaine",
    "Règne",
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
    
    def est_ascendant_de(self, autre):
        if autre is None:
            return False
        if self.nom == autre.nom:
            return True
        return self.est_ascendant_de(autre.parent)
    
    def set_parent(self, other):
        self.parent = other
    
    def asdict(self):
        return {
            "name": f"{self.rangTaxonomique}: {self.nom}",
            "children": sorted((child.asdict() for child in self.descendants), key=(lambda child: rangsTaxonomiques.index(child["name"].split(":")[0])))
        }

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
                        parent = noeud
                        noeud = noeuds[taxon]
                        if parent is None or noeud.parent is None:
                            continue
                        nouvel_index = rangsTaxonomiques.index(parent.rangTaxonomique)
                        ancien_index = rangsTaxonomiques.index(noeud.parent.rangTaxonomique)
                        if nouvel_index > ancien_index:
                            # cas 0 1 3 0 2 3
                            if noeud.parent.est_ascendant_de(parent):
                                noeud.parent.descendants.remove(noeud)
                                noeud.set_parent(parent)
                                parent.descendants.add(noeud)
                            else:
                                noeud.parent.descendants.remove(noeud)
                                noeud.parent.descendants.add(parent)
                                parent.parent = noeud.parent
                                noeud.set_parent(parent)
                                parent.descendants.add(noeud)


    with open("arbre.json", mode="w") as arbre:
        json.dump(eukariotes.asdict(), arbre)
    #exit()
    
    noeud = eukariotes
    liste_des_animo_aleratoire = random.choice(liste_des_animo)
    difficult = input("Difficulté normal ou hard ? \n")

    with open(f"data/{liste_des_animo_aleratoire}.json") as animal_aleatoire_content:
        classification = json.load(animal_aleatoire_content)["classification"][-1][1]
    if difficult == "normal":
        classification = f"{liste_des_animo_aleratoire}, {classification}"
        print("La difficulté selectionné est normal, le nom vernaculaire sera ajouté. \n")
    else: 
         print("La difficulté selectionné est hard, il n'y aura que le nom scientifique. \n") 
    print("Pour revenir en arrière : z", sep="\n")
    while True:
        listeDesDescendants = list(noeud.descendants)
        for k, d in enumerate(noeud.descendants):
            print(f"{d.nom} | {classification}")   
            print(f"{k}: {d} \n")
        choice = input()
        print("\n")
        if d.nom == classification :
            print("TU AS GAGNE BRAVO")
            break
        if choice == "z" and noeud.parent is not None:
            noeud = noeud.parent
        elif choice.isdigit():
            choice = int()
            if choice >= len(listeDesDescendants):
                print("Mauvais choix")
            else:
                noeud = listeDesDescendants[int(choice)]
        else:
            print("Mauvais choix")

                

