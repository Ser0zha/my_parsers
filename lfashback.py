import os
from pathlib import Path

import requests
from bs4 import BeautifulSoup


def separation_url(string: str) -> str:
    string = string.split('//')[1]
    final_string = str()
    for i in string:
        if i.isalpha():
            final_string += i
        else:
            break
    return final_string + '_' + 'content'


url = 'https://rostov-province.ru/'

response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

sel = soup.select('.wrap > ul > li > a')

Path("output").mkdir(parents=True, exist_ok=True)

filename = separation_url(url)
count = 0

for html in sel:

    link = html['href']
    resp = requests.get(url + str(link))
    bs = BeautifulSoup(resp.content, "html.parser")

    sel_2 = bs.select('.intro-body-content > .title > a')

    for html_2 in sel_2:

        link_of_link = html_2['href']
        respp = requests.get(url + str(link_of_link))
        bts = BeautifulSoup(respp.text, "html.parser")

        paragraphs = bts.select('.content-text')
        for i in paragraphs:
            file_os_name = os.path.join("output", f'{filename}_{count}.txt')
            with open(file_os_name, 'w', encoding='utf-8') as f:
                f.write(i.get_text('\n'))

        count += 1
