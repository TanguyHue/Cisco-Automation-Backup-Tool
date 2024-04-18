import curses

class ListeAvecCases:
    def __init__(self, items):
        self.items = items
        self.checked = [False] * len(items)
        self.selected_index = 0

    def afficher(self, stdscr):
        stdscr.clear()
        for i, item in enumerate(self.items):
            checked = 'X' if self.checked[i] else ' '
            if i == self.selected_index:
                stdscr.addstr(f"> [{checked}] {item}\n", curses.color_pair(1))
            else:
                stdscr.addstr(f"  [{checked}] {item}\n")

    def cocher_decocher(self, index):
        self.checked[index] = not self.checked[index]

    def executer(self, stdscr):
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        while True:
            self.afficher(stdscr)
            stdscr.addstr(len(self.items) + 1, 0, "Appuyez sur espace pour cocher/décocher, ou Entrée pour valider.")
            key = stdscr.getch()
            if key == curses.KEY_ENTER or key in [10, 13]:
                break
            elif key == curses.KEY_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.items)
            elif key == curses.KEY_UP:
                self.selected_index = (self.selected_index - 1) % len(self.items)
            elif key == ord(' '):
                self.cocher_decocher(self.selected_index)

# Exemple d'utilisation
if __name__ == "__main__":
    items = ["Item 1", "Item 2", "Item 3", "Item 4"]
    liste = ListeAvecCases(items)
    curses.wrapper(liste.executer)
