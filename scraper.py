#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019  <@localhost>
#
# Distributed under terms of the MIT license.

"""
yts scraper
"""
import settings
import main
SEARCH_LINK = settings.SEARCH_LINK
HOME_LINK = settings.HOME_LINK
PROXIES = main.PROXIES
DOWNLOAD_LINK = settings.DOWNLOAD_LINK
TITLE_CLASS = settings.TITLE_CLASS
import os
def check_dependencies(exe):
    try:
        __import__(exe)
    except ImportError:
          print(f"Trying to Install required module: {exe}\n")
          os.system(f'python3 -m pip install {exe}')

from re import compile
check_dependencies('requests')
from requests import get
check_dependencies('inquirer')
import inquirer
check_dependencies('bs4')
check_dependencies('html5lib')
from bs4 import BeautifulSoup



def get_movie(query):
    print("Getting Data...")
    response = get(SEARCH_LINK.replace('{query}', query), proxies=PROXIES)
    html = response.text
    soup = BeautifulSoup(html, 'html5lib')
    return soup.find_all(name='a',
                         attrs={'class': TITLE_CLASS}
                         )


def get_downloads(link):
    response = get(link, proxies=PROXIES)
    html = response.text
    soup = BeautifulSoup(html, 'html5lib')
    return soup.find_all('a',
                         attrs={'href': compile(f'^{DOWNLOAD_LINK}.*')})

def open_torrent(link):
    with open('tmp.torrent', 'wb+') as file:
        file.write(get(link, proxies=PROXIES).content)
    os.system('xdg-open tmp.torrent')

def main():
    print("Cant be used as a main script")



if __name__ == "__main__":
    main()
