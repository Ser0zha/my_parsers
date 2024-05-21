import os
from pathlib import Path
from typing import Any

import nltk
import requests
from bs4 import BeautifulSoup
from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize
from pymorphy2 import MorphAnalyzer
from requests import Response

nltk.download('punkt')


def fetch_html(base_url, category=None) -> Response:
    if category:
        url = f"{base_url}?category={category}"
    else:
        url = base_url

    response = requests.get(url)
    response.raise_for_status()

    return response


def get_categories(categories_url):
    html = fetch_html(categories_url)
    soup = BeautifulSoup(html.text, 'html.parser')
    categories = {}

    # FIXME: заменить на нормальный селектор
    for category_tag in soup.select('.category-class'):
        category_name = category_tag.text.strip()
        category_url = category_tag['href']
        categories[category_name] = category_url

    return categories


def text_correction_punctuation(lst: list[str]) -> str:
    result = ""
    for i in range(len(lst)):
        result += lst[i] + ' '
    return result


def lemmatized_text(txt: list[list[str]]):
    morph = MorphAnalyzer()
    lemma = []
    for inf in txt:
        a = [morph.parse(word)[0].normal_form for word in inf]
        lemma.append(a)
    return lemma


def get_topic_sentences(file_path: str, topic: str):
    morph = MorphAnalyzer()
    topic = morph.parse(topic)[0].normal_form
    list_with_suggestions1 = list()

    with open(file_path, 'r', encoding='utf-8', newline='\n') as file:
        text = file.read()

    # Разделение текста на предложения
    preprocessed_sentences = preprocess_text(sent_tokenize(text))

    original_text = sent_tokenize(text)

    fdist = FreqDist(preprocessed_sentences)

    # Выбор предложений, связанных с заданной темой
    topic_sentences = [original_text[i] for i, info in enumerate(preprocessed_sentences) if topic in info]

    # Вывод предложений, упорядоченных по частоте встречаемости
    for sentence in sorted(topic_sentences, key=lambda x: fdist[x], reverse=True):
        list_with_suggestions1.append(sentence)

    return list_with_suggestions1


def preprocess_text(sentences: Any) -> list[str]:
    # Удаление стоп-слов
    with open("stop_ru.txt", "r") as stop_ru:
        rus_stops = [word.strip() for word in stop_ru.readlines()]
    punctuation = '!\"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~—»«...–'
    fltr = rus_stops + list(punctuation)

    # Стемминг слов + Лемматизация
    clean_text = [word for word in sentences if word not in fltr]

    stemmed_sentences = []

    for sentence in clean_text:
        words = nltk.word_tokenize(sentence)
        stemmed_words = [word for word in words]
        stemmed_sentences.append(stemmed_words)

    # Лемматизация
    lemmatized = lemmatized_text(stemmed_sentences)
    lemmatized = list(map(text_correction_punctuation, lemmatized))

    return lemmatized


def separation_url(string: str) -> str:
    string = string.split('//')[1]
    final_string = str()
    for i in string:
        if i.isalpha():
            final_string += i
        else:
            break
    return final_string + '_' + 'content.txt'


def writerr(file_for_write, file_p: str, trigger=False) -> None:
    if trigger:
        with open(file_p, 'w', encoding='utf-8') as f:
            for paragraph in file_for_write:
                f.write(paragraph.get_text() + '\n')

    if not trigger:
        with open(file_p, "w", encoding='utf-8') as f:
            for i in file_for_write:
                f.write(i + '\n')


def search_info(resp: Response, address: str) -> None:
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        paragraphs = soup.find_all('p')
        # paragraphs = soup.find_all('article')

        writerr(paragraphs, address, trigger=True)
    else:
        print(f'Failed to fetch webpage:{resp.status_code}')
        exit()


def main(base_url: list[list[str]], category=None, output_dir='output') -> None:
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    for url, topic in base_url:
        filename = separation_url(url)

        file_os_name = os.path.join(output_dir, filename)

        html = fetch_html(url, category)

        search_info(html, file_os_name)

        sample = get_topic_sentences(file_os_name, topic)

        writerr(sample, file_os_name)

        print(f'Saved: {filename}')


if __name__ == "__main__":
    base_urls = [
        ['https://eastern-lands.blogspot.com/', 'игра'],
        ['https://u-96.livejournal.com/', 'смерть'],
        ['https://rostov-province.ru/', 'образование'],
        ['http://bereganews.ru/', 'экономика'],
        ['https://tutaev-gazeta.ru/', 'власть']
    ]
    main(base_urls)
