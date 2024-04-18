import curses

class ListeAvecCases:
    def __init__(self, items, one_checked=False, default_value=False):
        self.items = items
        self.checked = [default_value] * len(items)
        self.selected_index = 0
        self.one_checked = one_checked
        self.prev_selected_index = None

    def afficher(self, stdscr):
        for i, item in enumerate(self.items):
            checked = 'X' if self.checked[i] else ' '
            if self.one_checked:
                if i == self.selected_index:
                    stdscr.addstr(f"> [{checked}] {item['text']}\n", curses.color_pair(1))
                else:
                    stdscr.addstr(f"  [{checked}] {item['text']}\n")
            else:
                if i == self.selected_index:
                    stdscr.addstr(f"> ({checked}) {item['text']}\n", curses.color_pair(1))
                else:
                    stdscr.addstr(f"  ({checked}) {item['text']}\n")

    def cocher_decocher(self, index):
        if self.one_checked:
            # Uncheck the previously selected interface (if any)
            if self.prev_selected_index is not None:
                self.checked[self.prev_selected_index] = False
            # Check the newly selected interface
            self.checked[index] = True
            # Update the previously selected index
            self.prev_selected_index = index
        else:
            self.checked[index] = not self.checked[index]

    def executer(self, stdscr):
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Liste des appareils détectés\n\n")
            self.afficher(stdscr)
            stdscr.addstr(len(self.items) + 3, 0, "Appuyez sur espace pour cocher/décocher, ou Entrée pour valider.")
            key = stdscr.getch()
            if (key == curses.KEY_ENTER or key in [10, 13])  and (not self.one_checked or self.prev_selected_index) is not None:
                break
            elif key == curses.KEY_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.items)
            elif key == curses.KEY_UP:
                self.selected_index = (self.selected_index - 1) % len(self.items)
            elif key == ord(' '):
                self.cocher_decocher(self.selected_index)