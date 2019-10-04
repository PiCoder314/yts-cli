#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019  <@localhost>
#
# Distributed under terms of the MIT license.

# -*- coding: utf-8 -*-
"""
    yts-cli.scraper
    ~~~~~~~~~~~~~~~

    YTS.AM website scraper

    :license: MIT, see LICENSE for more details.
"""

def check_dependencies(exe):
    try:
        __import__(exe)
    except ImportError:
        print(f"Trying to Install required module: {exe}\n")
        os.system(f'python3 -m pip install {exe}')

# Dependency Check
check_dependencies('requests')
check_dependencies('inquirer')
check_dependencies('bs4')
check_dependencies('lxml')
# Pip Modules
import re
from bs4 import BeautifulSoup
import inquirer
import requests

# Custom Modules
import settings
import sys
import os
# Global Variables
SEARCH_LINK = settings.SEARCH_LINK
HOME_LINK = settings.HOME_LINK
DOWNLOAD_LINK = settings.DOWNLOAD_LINK
TITLE_CLASS = settings.TITLE_CLASS
YEAR_CLASS = settings.YEAR_CLASS




def get_movie(query):
    """ 
    Description: Get movies by search term
    Args: query
    """
    PROXIES = settings.PROXIES

    try:
        response = requests.get(SEARCH_LINK.replace('{query}', query), proxies=PROXIES)
    except requests.exceptions.ProxyError:
        print('ProxyError please try again later.\nWe recommend to use a VPN.')
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print('Use the proxy flag or a VPN')
        sys.exit(1)
    html = response.text

    soup = BeautifulSoup(html, 'lxml')

    movies_info = {}

    movies_info['tags'] = soup.find_all(name='a',
            attrs={'class': TITLE_CLASS}
            )

    movies_info['names'] = []
    movies_info['links'] = []
    movies_info['years'] = []

    for tag in movies_info['tags']:
        movies_info['names'].append(tag.string)
        movies_info['links'].append(tag.get('href'))

    movies_info['year_tags'] = soup.find_all(name='div',
            attrs={'class': YEAR_CLASS}
            )
    for tag in movies_info['year_tags']:
        movies_info['years'].append(tag.string)

    movies = []

    for i, info in enumerate(movies_info['names']):
        movies.append({
            "name": movies_info['names'][i],
            "link": movies_info['links'][i],
            "year": movies_info['years'][i]
            })

    return movies


def get_downloads(link):
    """ 
    Description: Get download links by movie link
    Args: link
    """

    PROXIES = settings.PROXIES
    try:
        response = requests.get(link, proxies=PROXIES)
    except requests.exceptions.ProxyError:
        print('ProxyError please try again later.\nWe recommend to use a VPN.')
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print('Use the proxy flag or a VPN')
        sys.exit(1)
    html = response.text

    soup = BeautifulSoup(html, 'lxml')

    links = soup.find_all('a',
                         attrs={'href': re.compile(f'^{DOWNLOAD_LINK}.*')})

    return links


def open_torrent(link):
    """ 
    Description: Download torrent file by link
    Args: link
    """
    PROXIES = settings.PROXIES
    with open('tmp.torrent', 'wb+') as file:
        try:
            file.write(requests.get(link, proxies=PROXIES).content)
        except requests.exceptions.ProxyError:
            print('ProxyError please try again later.\nWe recommend to use a VPN.')
            sys.exit(1)
        except requests.exceptions.ConnectionError:
            print('Use the proxy flag or a VPN')
            sys.exit(1)
    os.system(settings.OPEN_COMMAND)


def main():
    print("Cant be used as a main script")


if __name__ == "__main__":
    main()
