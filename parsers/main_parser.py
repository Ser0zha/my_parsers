import requests
from bs4 import BeautifulSoup
from parsers.base_parser import BaseParser


class Parser(BaseParser):
    def fetch_html(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return response

    def get_categories(self, categories_url: str, path_for_cat: str):
        html = self.fetch_html(categories_url)

        if html.status_code == 200:
            soup = BeautifulSoup(html.content, 'html.parser')
            categories = soup.select(path_for_cat)
            return categories
        else:
            print(f'Failed to fetch webpage:{html.status_code}')
            exit()

    def parse_html(self, sel, url):

        link = sel['href']
        resp = requests.get(url + str(link))
        soup = BeautifulSoup(resp.content, "html.parser")
        return soup
