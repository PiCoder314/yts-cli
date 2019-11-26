import curses
import curses.panel
from widgets import menu, form
from stf import *
import yts_scraper

ROWS = COLS = None
stdscr = None
render = True
running = True


def init_screen():
    global ROWS, COLS, stdscr
    stdscr = curses.initscr()
    ROWS, COLS = stdscr.getmaxyx()
    curses.cbreak()


def init_colors():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_GREEN, -1)



def quit():
    global running
    running = False


def mainloop():
    global render
    global stdscr, ROWS, COLS
    while running:
        stdscr.clear()
        curses.noecho()
        curses.curs_set(0)
        space.listen()
    stdscr.clear()
    curses.curs_set(1)
    curses.endwin()


if __name__ == "__main__":
    init_screen()
    init_colors()
    title_window = curses.newwin(6, COLS, 0, 0)
    title_window.addstr("""
    ░█░█░▀█▀░█▀▀
    ░░█░░░█░░▀▀█
    ░░▀░░░▀░░▀▀▀\n""", curses.color_pair(2))
    for _ in range(title_window.getmaxyx()[1]):
        title_window.addstr(u'\u2500')
    title_panel = curses.panel.new_panel(title_window)
    space = form.Form(0, 5, ROWS-7, COLS)
    space.set_title("Movies")
    movies = menu.Menu(space.win, ["Press q tp quit", "Press / to search a movie", "More features coming soon"])
    space.add_widget(movies)


    mainloop()

    curses.endwin()


