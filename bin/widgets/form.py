import curses


class Form():
    global render
    def __init__(self, x, y, height, width):
        self.win = curses.newwin(height, width, y, x)
        self.panel = curses.panel.new_panel(self.win)
        self.widgets = list()


    def add_widget(self, wid):
        self.widgets.append(wid)
        self.update()


    def update(self):
        for widget in self.widgets:
            widget.render()
        render = True


    def listen(self):
        for widget in self.widgets:
            widget.listen()


    def set_title(self, title, char=u'\u2500'):
        rows, cols = self.win.getmaxyx()
        self.win.move(1, 0)
        self.win.addstr(char)
        self.win.addstr(title)
        for _ in range(1, cols-len(title)):
            self.win.addstr(char)
        self.win.addstr('\n')
        render = True


    def render(self):
        pass
