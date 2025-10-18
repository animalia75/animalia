import os
import sys
import lxml.html as lhtml
import json
import traceback

list_url = "https://fr.wikipedia.org/wiki/Portail%3AMammif%C3%A8res%2FListe_alphab%C3%A9tique_des_noms_vernaculaires_de_mammif%C3%A8res"

base_url = "https://fr.m.wikipedia.org"
image_pattern = "Description de cette image, également commentée ci-après"
file_path = ".\\data"


def curl(url, dest_file_name):
    os.system(f'powershell -command "curl \\"{url}\\" -OutFile \\"{dest_file_name}\\""')


def get_image_url(html):
    return next(filter(
        lambda img: img.get("alt") == image_pattern,
        html.xpath('//img')
    )).get("src")


def get_classification(html):
    elements = next(filter(
        lambda table: table.get("class") == "taxobox_classification",
        html.xpath('//table')
    )).xpath('//tbody')[0].xpath('.//tr')

    return [(
        element.getchildren()[0].xpath('.//a')[0].text_content(),
        element.getchildren()[1].xpath('.//a')[0].text_content()
        ) for element in elements
    ]


def get_additional_classification(html):
    res = []
    for attribute, value in zip(
        filter(
            lambda div: div.get("class") == "bloc",
            html.xpath('//p')
        ),
        filter(
            lambda div: div.get("class") == "center taxobox_classification",
            html.xpath('//div')
        )
    ):
        res.append((attribute.text_content(), value.xpath('.//b')[0].xpath('.//span')[0].text_content()))
    return res


def get_list_species():
    res = []
    file_name = f"{file_path}\\list.html"
    # curl(list_url, file_name)
    with open(file_name, "r", encoding="utf8") as file:
        html = lhtml.fromstring(file.read())
        species_list_list = list(filter(
            lambda div: div.get("class") == "colonnes",
            html.xpath('//div')
        ))

        for species_list in species_list_list:
            for species in species_list.xpath('.//a'):
                res.append((
                    species.text_content().replace(" ", "_"),
                    species.get("href")
                ))
    return res



def main():
    list_species = get_list_species()
    worked_list_species = []
    try:
        for name, link in list_species:
            file_name = f"{file_path}\\{name}"
            # curl(f"{base_url}{link}", f"{file_name}.html")
            try:
                with open(f"{file_name}.html", "r", encoding="utf8") as file:
                    html = lhtml.fromstring(file.read())
                    # curl(f"https:{get_image_url(html)}", f"{file_name}.jpg")
                    classification = get_classification(html)
                    classification += get_additional_classification(html)
                    with open(f"{file_name}.json", "w", encoding="utf8") as json_file:
                        jsonContent = {
                            "imgUrl": f"https:{get_image_url(html)}",
                            "pageUrl": f"{base_url}{link}",
                            "classification":classification 
                        }
                        json_file.write(json.dumps(jsonContent))
                worked_list_species.append(name)

            except Exception as e:
                os.system(f'del {file_name}.*')
                exc_type, exc_value, exc_traceback = sys.exc_info()
                with open(f'{file_name}.error', "w", encoding="utf8") as file:
                    file.write(str(traceback.format_exc()))
                continue
    finally:
        # os.system(f'del {file_path}\\*.html')
        with open(f"{file_path}\\list.json", "w", encoding="utf8") as json_file:
            json_file.write(json.dumps(worked_list_species))

if __name__ == "__main__":
    main()


