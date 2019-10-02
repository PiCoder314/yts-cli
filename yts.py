#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019  <@localhost>
#
# Distributed under terms of the MIT license.

""" yts scraper """
import sys
import settings
import getopt
import scraper
import inquirer


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
                settings.PROXIES = {
                        'http': 'http://35.236.147.162:80',
                        'https': 'https://103.224.5.5:54143'
                        }

    except getopt.GetoptError:
        print('usage: ./main.py [query] [options]\noptions\n-q, --query= : movie to search for\n-p,--use-proxy: use anonymous proxy')

    if 'query' not in locals():
        query = input('Enter movie name: ')

    print(f"Searching for {query}...")
    links = scraper.get_movie(query)
    if len(links[0]) == 0:
        print('No movies found check the spelling')
        return 1

    questions = [
            inquirer.List('movie',
                'Choose a movie to download?',
                list(map(lambda x: x[0].string + " (" + x[1].string + ")", links))
                )
            ]
    answers = inquirer.prompt(questions)
    answers = answers['movie'].split('(', 1)[0][:-1]
    print('Getting Download Links...')
    link = list(filter(lambda x: x[0].string == answers, links))[0][0].get('href')
    print(link)
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
    scraper.open_torrent(link)
    print("Link:", link)


if __name__ == "__main__":
    main()
