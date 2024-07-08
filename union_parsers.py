import os
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup
from bs4 import ResultSet
from requests import Response


def separation_url(string: str) -> str:
    '''
    :param string:

    :return: Строчку с названием сайта, чтобы легче было понять откуда + индивидуальность
    '''
    string = string.split('//')[1]
    final_string = str()
    for i in string:
        if i.isalpha():
            final_string += i
        else:
            break
    return final_string + '_' + 'content'


def fetch_html(base_url: str) -> Response:
    response = requests.get(base_url)
    response.raise_for_status()
    return response


def main_parser(ready_topics: ResultSet) -> None:
    '''
    Парсер, с помощью которого будем переходить по темам, которые уже имеются
    :param ready_topics: все темы, которые удалось запарсить
    :return: НИЧЕГО =)
    '''
    def parsing_in_depth(sel, code: int = 0, count: int = 0):
        '''
        Ничего необычного просто функция, для того, чтобы было удобнее парсить и при этом не писать какие-то
        вложенные циклы (хотя такие получились =( )
        :param sel: Сокращение от Select, вся инфа из тэгов <a> </a>
        :param code: просто переключатель если можно так сказать (так как имеем 2 ур вложенности у сайта)
        :param count: счётчик для функций saves
        :return:
        '''
        link = sel['href']
        resp = requests.get(url + str(link))
        bs = BeautifulSoup(resp.content, "html.parser")

        if code == 0:
            sel = bs.select('.intro-body-content > .title > a')
            if not sel:
                sel = bs.select('.content-wrap > .title')
            return sel

        else:
            sel = bs.select('.content-text')
            if not sel:
                sel = bs.select('.item-content')
            saves(sel, count, topic.text)

    for topic in ready_topics:
        a = parsing_in_depth(topic)
        for count, i in enumerate(a):
            parsing_in_depth(i, code=1, count=count)
    print('end')


def parser(url_addres: str) -> ResultSet:
    '''
    Парсер для тем, ссайта
    :param url_addres: ссылка на сайт для парсинга
    :return: вернём специальный ответ, с полной информацией о темах и href ссылках
    '''
    respons = fetch_html(url_addres)
    if respons.status_code == 200:
        soup = BeautifulSoup(respons.content, "html.parser")
        sel = soup.select('.wrap > ul > li > a')
        return sel
    else:
        print(f'Failed to fetch webpage:{respons.status_code}')
        exit()


def saves(paragraphs: Any, count: int, theme: str) -> None:
    '''
    :param paragraphs: текст, который будем сохранять на диск
    :param count: простой счётчик для того, чтобы у файлов были свои имена
    :param theme: тема, под которую будет создаваться уникальная директория
    :return:
    '''

    Path(theme).mkdir(parents=True, exist_ok=True)

    global filename
    for i in paragraphs:
        file_os_name = os.path.join(theme, f'{filename}_{count}.txt')
        with open(file_os_name, 'w', encoding='utf-8') as f:
            txt = i.text.replace(". ", '\n')
            f.write(txt)


def main() -> None:
    global filename

    filename = separation_url(url)
    topics = parser(url)
    main_parser(topics)


if __name__ == "__main__":
    url = 'https://tutaev-gazeta.ru/'
    filename: str
    main()
