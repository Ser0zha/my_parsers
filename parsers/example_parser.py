import requests
from bs4 import BeautifulSoup
from parsers.base_parser import BaseParser


class Parser(BaseParser):
    def fetch_html(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    def get_categories(self, categories_url):
        html = self.fetch_html(categories_url)
        soup = BeautifulSoup(html, 'html.parser')
        categories = {}
        for category_tag in soup.select('.category-class'):  # заменить на правильный CSS-селектор
            category_name = category_tag.text.strip()
            category_url = category_tag['href']
            categories[category_name] = category_url
        return categories

    def parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        articles = soup.find_all('article')
        texts = [article.get_text() for article in articles]
        return texts
