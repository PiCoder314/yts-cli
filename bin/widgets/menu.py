import curses
from stf import *
import yts_scraper
import os


class Menu():
    def __init__(self, window, items):
        self.window = window
        self.items = items
        self.active_index = 0
        self.window.nodelay(1)
        self.window.keypad(1)
        self.movies = None
        self.links = None
        self.down = False


    def cycle(self, _dir):
        if _dir > 0:
            if self.active_index == len(self.items)-1:
                self.active_index = 0
            else:
                self.active_index += 1
        else:
            if self.active_index == 0:
                self.active_index = len(self.items)-1
            else:
                self.active_index -= 1
        self.render()

    def listen(self):
        global running
        curses.noecho()
        key = self.window.getch()
        if key > 0:
            # down arrow
            if key == 258 or chr(key) == 'j':
                self.window.clear()
                self.cycle(1)
            # up arrow
            if key == 259 or chr(key) == 'k':
                self.window.clear()
                self.cycle(-1)
            if key == curses.KEY_ENTER or key == 10 or key == 13:
                self.window.clear()
                if not self.down:
                    self.get_links()
                    self.down = True
                else:
                    yts_scraper.open_torrent(self.links[self.active_index])
                    self.items = ["Press / to search.",]
                    self.down = False
                    self.render()
            if chr(key) == '/':
                self.window.clear()
                self.search()
            if chr(key) == 'q':
                curses.curs_set(2)
                curses.endwin()
                quit()


    def get_links(self):
        self.links = yts_scraper.get_downloads(self.movies[self.active_index].link)
        self.items = [link.string for link in self.links if link.string]
        self.window.addstr(str(self.items))
        self.links = [link.get('href') for link in self.links if link.string]
        self.render()

    def search(self):
        curses.curs_set(1)
        search_str = ""
        rows, cols = self.window.getmaxyx()
        self.window.move(rows-1, 0)
        self.window.addstr('/' + pad(search_str, cols-2, " "))
        self.render()
        key = None
        while key != 27:
            key = self.window.getch()
            if key > 0:
                if key == 127:
                    if search_str != "":
                        search_str = search_str[:-1]
                        self.window.move(rows-1, 0)
                        self.window.addstr(pad(search_str, cols-1, " "))
                        self.window.move(rows-1, 0)
                        self.window.addstr('/' + search_str)
                        self.render()
                    else:
                        self.window.move(rows-1, 0)
                        self.window.addstr(pad(search_str, cols-1, " "))
                        self.render()
                        break
                elif key == curses.KEY_ENTER or key == 10 or key == 13:
                    self.window.move(rows-1, 0)
                    self.window.addstr(pad(f'Searching for {search_str}...', cols-1, " "))
                    self.render()
                    self.movies = yts_scraper.get_movie(search_str)
                    self.items = self.get_name()
                    self.window.move(rows-1, 0)
                    self.window.addstr(pad(" ", cols-1, " "))
                    self.window.clear()
                    self.render()
                    break
                else:
                    search_str += chr(key)
                    self.window.move(rows-1, 0)
                    self.window.addstr(pad(search_str, cols-1, " "))
                    self.window.move(rows-1, 0)
                    self.window.addstr('/' + search_str)
                    self.render()
        curses.curs_set(0)


    def get_name(self):
        lst = []
        for movie in self.movies:
            lst.append(f'{movie.name} ({movie.year})')
        return lst


    def render(self):
        y,x = self.window.getyx()
        rows, cols = self.window.getmaxyx()
        self.window.move(0,0)
        for item in self.items:
            if item == self.items[self.active_index]:
                item = pad(item, cols - 1, " ")
                self.window.addstr(' ' + item, curses.color_pair(1) + curses.A_BOLD)
            else:
                item = pad(item, cols - 1, " ")
                self.window.addstr(' ' + item)
        self.window.move(y,x)
        curses.panel.update_panels()
        curses.doupdate()
