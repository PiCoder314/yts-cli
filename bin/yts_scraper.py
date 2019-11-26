#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
import sys
import os

# Pip Modules
import re
from bs4 import BeautifulSoup
import inquirer
import requests

# Custom Modules
import settings

# Global Variables
SEARCH_LINK = settings.SEARCH_LINK
BASE_LINK = settings.BASE_LINK
DOWNLOAD_LINK = settings.DOWNLOAD_LINK
TITLE_CLASS = settings.TITLE_CLASS
YEAR_CLASS = settings.YEAR_CLASS




class Movie():

    """Docstring for Movie. """

    def __init__(self, name="", year="", link=""):
        self.name = name
        self.year = year
        self.link = link
    def set_name(self, name):
        self.name = name
    def set_year(self, year):
        self.year = year
    def set_link(self, link):
        self.link = link
    def get_link(self):
        return self.link
    def get_name(self):
        return self.name
    def get_year(self):
        return self.year
        

def get_movie(query):
    PROXIES = settings.PROXIES
    try:
        response = requests.get(SEARCH_LINK.replace('{query}', query), proxies=PROXIES)
        html = response.text
    except requests.exceptions.ProxyError:
        print('ProxyError please try again later.\n' +
              'We recommend to use a VPN.')
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print('Use the proxy flag or a VPN')
        sys.exit(1)

    soup = BeautifulSoup(html, 'html.parser')

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
        movie = Movie()
        movie.set_name(movies_info['names'][i])
        movie.set_year(movies_info['years'][i])
        movie.set_link(movies_info['links'][i])
        movies.append(movie)

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

    soup = BeautifulSoup(html, 'html.parser')

    links = soup.find_all('a',
                         attrs={'href': re.compile(f'^{DOWNLOAD_LINK}.*')})

    return links


def open_torrent(link):
    """ 
    Description: Download torrent file by link
    Args: link
    """
    PROXIES = settings.PROXIES
    with open('./files/tmp.torrent', 'wb+') as file:
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
