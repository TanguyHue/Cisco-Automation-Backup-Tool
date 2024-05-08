import curses

class ListeAvecCases:
    def __init__(self, items, text='', one_checked=False, default_value=False):
        self.items = items
        self.text = text + "\n\n"
        self.checked = [default_value] * len(items)
        self.selected_index = 0
        self.one_checked = one_checked
        self.prev_selected_index = None

    def afficher(self, stdscr):
        if self.items == []:
            stdscr.addstr("No item to display.")
            return
        for i, item in enumerate(self.items):
            checked = 'X' if self.checked[i] else ' '
            if self.one_checked:
                if i == self.selected_index:
                    stdscr.addstr(f"> {item.get_text()}\n", curses.color_pair(1))
                else:
                    stdscr.addstr(f"  {item.get_text()}\n")
            else:
                if i == self.selected_index:
                    stdscr.addstr(f"> ({checked}) {item.get_text()}\n", curses.color_pair(1))
                else:
                    stdscr.addstr(f"  ({checked}) {item.get_text()}\n")

    def cocher_decocher(self, index):
        if self.one_checked:
            if self.prev_selected_index is not None:
                self.checked[self.prev_selected_index] = False
            self.checked[index] = True
            self.prev_selected_index = index
        else:
            self.checked[index] = not self.checked[index]

    def executer(self, stdscr):
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, self.text)
            self.afficher(stdscr)
            if self.one_checked:
                stdscr.addstr(len(self.items) + 3, 0, "Press 'Enter' to validate.")
            else:
                stdscr.addstr(len(self.items) + 3, 0, "Press 'Space' to check/uncheck an item, 'Enter' to validate.")
            key = stdscr.getch()
            if (key == curses.KEY_ENTER or key in [10, 13])  and (not self.one_checked or self.prev_selected_index) is not None:
                break
            if (key == curses.KEY_ENTER or key in [10, 13] or key == ord(' ')) and self.one_checked:
                self.cocher_decocher(self.selected_index)
                break
            elif key == curses.KEY_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.items)
            elif key == curses.KEY_UP:
                self.selected_index = (self.selected_index - 1) % len(self.items)
            elif key == ord(' '):
                self.cocher_decocher(self.selected_index)
                if self.one_checked:
                    break