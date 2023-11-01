import re

import matplotlib.pyplot as plt

from load_and_extract import ComedianHtmlParser


def extract_number(text: str) -> int:
    pattern = r'\d+'
    matched = re.findall(pattern, text)
    number = int(matched[0]) if matched else 0
    return number
    

def filter_properties_for_graph(profile: dict[str, str]) -> dict[str, str]:
    return {'age': extract_number(profile['age']), 'years': extract_number(profile['years']),
            'name': profile['name'], 'group': profile['group']}


def show_scatter(profiles) -> None:
    names = []
    ages = []
    years = []

    for profile in profiles:
        names.append(profile['name'])
        ages.append(profile['age'])
        years.append(profile['years'])

    plt.scatter(ages, years)

    for i, name in enumerate(names):
        plt.text(ages[i], years[i], name)
    
    plt.show()
        

if __name__ == '__main__':
    comedian_html_parser = ComedianHtmlParser('./profiles.html')
    profiles = comedian_html_parser.extract_profiles_from_html_doc()

    formatted_profiles = list(map(
        lambda profile: filter_properties_for_graph(profile), profiles))

    # Japanese is not displayed and data is too much to show
    show_scatter(formatted_profiles)
