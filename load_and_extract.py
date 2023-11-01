import re

from bs4 import BeautifulSoup


class HtmlParser:
    def __init__(self, path_to_html: str) -> None:
        self.path_to_html = path_to_html
        self.html_doc = self.load_html(path_to_html)

    def load_html(self, path_to_html: str) -> str:
        with open(path_to_html, 'r', encoding='utf-8') as html_file:
            html_doc = html_file.read()
            return html_doc


class ComedianHtmlParser(HtmlParser):
    def __init__(self, path_to_html: str) -> None:
        super().__init__(path_to_html)

    def extract_profiles_from_html_doc(self) -> list[str]:
        soup = BeautifulSoup(self.html_doc, 'html.parser')
        gprofile_blocks = soup.find_all('div', class_='gprofile')
        gprofile_blocks = gprofile_blocks[1:]

        profiles = []
        for gprofile_block in gprofile_blocks:
            if len(gprofile_block.find_all('span')) > 1:
                years = gprofile_block.find('span', class_='c01').text
                name_and_group = gprofile_block.find('span', class_='c02').text
                name = self.remove_parentheses_from_text(name_and_group)
                group = self.extract_text_inner_parentheses(name_and_group)
                debut = gprofile_block.find('span', class_='c03').text
                organization = gprofile_block.find('span', class_='c04').text
                age = gprofile_block.find('span', class_='c05').text
                birth_date = gprofile_block.find('span', class_='c06').text
                others = gprofile_block.find('span', class_='c07').text
                profile = {
                    'years': years,
                    'name': name,
                    'group': group,
                    'debut': debut,
                    'organization': organization,
                    'age': age,
                    'birth': birth_date,
                    'others': others
                }
                profiles.append(profile)
        return profiles

    def remove_parentheses_from_text(self, text: str) -> str:
        pattern = r'（.*?）'
        replaced_text = re.sub(pattern, '', text)
        return replaced_text

    def extract_text_inner_parentheses(self, text: str) -> str:
        pattern = r'（(.*?)）'
        matched = re.search(pattern, text)
        text_inside_parentheses = matched.group(1) if matched else 'no'
        return text_inside_parentheses
