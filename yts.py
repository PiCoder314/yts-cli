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
import os


# Main Function
def main():
    # Check for command line arguments
    try:
        args = sys.argv[1:]
        opts, args = getopt.getopt(args, 'hq:pcd', ['query=', 'use-proxy', 'use-cli'])
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                print('usage: ./main.py [query] [options]\noptions\n-q, --query= : movie to search for\n-p,--use-proxy : use anonymous proxy')
                return 0
            if opt in ('-q', '--query'):
                query=arg
            if opt in ('-p', '--use-proxy'):
                settings.PROXIES = {
                        'http': 'http://35.236.147.162:80',
                        'https': 'https://103.224.5.5:54143'
                        }
            if opt in ('-c', '--use-cli'):
                settings.OPEN_COMMAND = 'aria2c tmp.torrent'

    except getopt.GetoptError:
        print('usage: ./main.py [query] [options]\noptions\n-q, --query= : movie to search for\n-p,--use-proxy: use anonymous proxy\n-c, --use-cli : use aria2 to download torrent')

    if 'query' not in locals():
        query = input('Enter movie name: ')

    # Get movies for yts.am
    print(f"Searching for {query}...")
    movies = scraper.get_movie(query)
    if len(movies) == 0:
        print('No movies found check the spelling')
        return 1

    # Prompt to choose movie
    print('Choose a movie to download')
    questions = [
            inquirer.List('movie',
                '==> ',
                [f"{movie['name']} ({movie['year']})" for movie in movies],
                carousel=True
                )
            ]
    answers = inquirer.prompt(questions)
    answer = answers['movie'].split('(', 1)[0][:-1]

    # Get download links for choosen movie
    print('Getting Download Links...')
    link = [movie['link'] for movie in movies if movie['name'] == answer][0]
    print(link)

    # Get download links from scraper
    links = scraper.get_downloads(link)
    links = [link for link in links if link.string != None]

    # Prompt to choose download quality
    print('Choose a quality to download')
    questions = [
            inquirer.List('quality',
                '==> ',
                [link.string for link in links],
                carousel=True
                )
            ]

    answers = inquirer.prompt(questions)
    link = list(filter(lambda x: x.string == answers['quality'], links))[0].get('href')

    # Download the torrent file and prompt to open
    scraper.open_torrent(link)
    print("Link:", link)


if __name__ == "__main__":
    try:
        main()
    # Handle keyboard interrupt
    except KeyboardInterrupt:
        print('User Interrupt')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
