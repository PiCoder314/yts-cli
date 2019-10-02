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
import settings
import getopt
import scraper
import inquirer
SEARCH_LINK = settings.SEARCH_LINK
HOME_LINK = settings.HOME_LINK
DOWNLOAD_LINK = settings.DOWNLOAD_LINK
TITLE_CLASS = settings.TITLE_CLASS
PROXIES={}


def main():
    try:
        args = sys.argv[1:]
        opts, args = getopt.getopt(args, 'hq:pd', ['query=', 'use-proxy'])
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                print('usage: ./main.py [query] [options]\noptions\n-q, --query= : movie to search for\n-p,--use-proxy : use anonymous proxy')
            if opt in ('-q', '--query'):
                query=arg
            if opt in ('-p', '--use-proxy'):
                PROXIES = settings.PROXIES

    except getopt.GetoptError:
        print('usage: ./main.py [query] [options]\noptions\n-q, --query= : movie to search for\n-p,--use-proxy: use anonymous proxy')

    if 'query' not in locals():
        query = input('Enter movie name: ')

    print(f"Searching for {query}...")
    links = scraper.get_movie(query)
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
    link = list(filter(lambda x: x.string == answers['movie'], links))[
        0].get('href')
    links = scraper.get_downloads(link)
    links = list(filter(lambda x: x.string != None, links))
    questions = [
        inquirer.List('quality',
                      'Choose a quality to download?',
                      list(map(lambda x: x.string, links))
                      )
    ]
    answers = inquirer.prompt(questions)
    link = list(filter(lambda x: x.string == answers['quality'], links))[
        0].get('href')
    open_torrent(link)
    print("Link:", link)


if __name__ == "__main__":
    main()
