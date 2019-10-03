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
        opts, args = getopt.getopt(args, 'hq:pd', ['query=', 'use-proxy'])
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

    except getopt.GetoptError:
        print('usage: ./main.py [query] [options]\noptions\n-q, --query= : movie to search for\n-p,--use-proxy: use anonymous proxy')

    if 'query' not in locals():
        query = input('Enter movie name: ')

    # Get movies for yts.am
    print(f"Searching for {query}...")
    links = scraper.get_movie(query)
    if len(links) == 0:
        print('No movies found check the spelling')
        return 1

    # Prompt to choose movie
    questions = [
            inquirer.List('movie',
                'Choose a movie to download?',
                list(map(lambda x: x[0].string + " (" + x[1].string + ")", links)),
                carousel=True
                )
            ]
    answers = inquirer.prompt(questions)
    answers = answers['movie'].split('(', 1)[0][:-1]
    # Get download links for choosen movie
    print('Getting Download Links...')
    link = list(filter(lambda x: x[0].string == answers, links))[0][0].get('href')
    print(link)
    links = scraper.get_downloads(link)
    links = list(filter(lambda x: x.string != None, links))
    # Prompt to choose download quality
    questions = [
            inquirer.List('quality',
                'Choose a quality to download?',
                list(map(lambda x: x.string, links)),
                carousel=True
                )
            ]
    answers = inquirer.prompt(questions)
    link = list(filter(lambda x: x.string == answers['quality'], links))[
            0].get('href')
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
