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
import sys
from scraper import *

def main():
    if (len(sys.argv) == 2):
        search = sys.argv[1]
    elif(len(sys.argv) > 2):
        print("usage: ./main.py <search-term>")
        return 1
    else:
        search = input('Enter movie name to search: ')
    print(f"Searching for {search}...")
    links = get_movie(search)
    if len(links) == 0:
        print('No movies found check the spelling')
        return 1

    questions = [
        inquirer.List('movie',
                      'Choose a movie to download?',
                      list(map(lambda x: x.string, links))
                      )
    ]
    answers = inquirer.prompt(questions)
    link = list(filter(lambda x: x.string == answers['movie'], links))[0].get('href')
    links = get_downloads(link)
    links = list(filter(lambda x: x.string != None, links))
    questions = [
        inquirer.List('quality',
                      'Choose a quality to download?',
                      list(map(lambda x: x.string, links))
                      )
    ]
    answers = inquirer.prompt(questions)
    link = list(filter(lambda x: x.string == answers['quality'], links))[0].get('href')
    open_torrent(link)
    print("Link:", link)


if __name__ == "__main__":
    main()
