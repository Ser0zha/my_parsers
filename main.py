import os
from pathlib import Path
from typing import Any

from bs4 import ResultSet

from parsers import main_parser as mp
import time
import random


def separation_url() -> str:
    string = url
    string = string.split('//')[1]
    final_string = str()
    for i in string:
        if i.isalpha():
            final_string += i
        else:
            break
    return final_string + '_' + 'content'


def my_parser(ready_topics: ResultSet) -> None:

    def parsing_in_depth(sel, code: int = 0, count: int = 0, ):

        clas = mp.Parser()
        bs = clas.parse_html(sel, url)

        if code == 0:
            sel = bs.select('.intro-body-content > .title > a')
            if not sel:
                sel = bs.select('.content-wrap > .title')
            elif not sel:
                sel = bs.select('.item-wrap > .title')
            return sel

        else:
            sel = bs.select('.content-text')
            if not sel:
                sel = bs.select('.item-content')
            saves(sel, count, topic.text)

    for topic in ready_topics:
        a = parsing_in_depth(topic)
        for count, i in enumerate(a):
            print(f'Тема: {topic.text}, номер статьи - {count}')
            parsing_in_depth(i, code=1, count=count)
            
        secs = random.randint(1, 11)
        time.sleep(secs)

    print('end')


def parser() -> ResultSet:
    pars = mp.Parser()
    path = '.wrap > ul > li > a'
    selects = pars.get_categories(url, path)
    return selects


def saves(paragraphs: Any, count: int, theme: str) -> None:
    Path(theme).mkdir(parents=True, exist_ok=True)

    for i in paragraphs:
        file_os_name = os.path.join(theme, f'{filename}_{count}.txt')
        with open(file_os_name, 'w', encoding='utf-8') as f:
            txt = i.text.replace(". ", '\n')
            f.write(txt)


def main() -> None:
    global filename

    filename = separation_url()
    topics = parser()
    my_parser(topics)


if __name__ == "__main__":
    url: str = 'https://rostov-province.ru/'
    filename: str
    main()
