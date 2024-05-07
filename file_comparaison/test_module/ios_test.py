import curses
from difflib import unified_diff
from sys import path

path.append("../..")

def read_files():
    try:
        with open('file_comparaison/test_module/cisco/s1.ios', 'r') as file_a:
            a = file_a.read()
        with open('file_comparaison/test_module/cisco/s2.ios', 'r') as file_b:
            b = file_b.read()
    except FileNotFoundError:
        return None, None
    return a, b

def main(stdscr):
    # Initialiser le support de couleur
    if curses.has_colors():
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)  # pour les lignes supprimées
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # pour les lignes ajoutées

    curses.curs_set(0)  # Cacher le curseur
    stdscr.clear()

    a, b = read_files()
    if a is None or b is None:
        stdscr.addstr("File not found\n")
        stdscr.refresh()
        stdscr.getch()
        return

    diff = unified_diff(a.splitlines(), b.splitlines(), n=20)
    diff_lines = list(diff)[3:]
    filtered_diff = [line for line in diff_lines if not line.startswith("@@")]

    index = 0
    max_lines = curses.LINES - 1  # Soustraire 1 pour la ligne de statut / d'info

    while True:
        stdscr.clear()
        for i in range(max_lines):
            if index + i < len(filtered_diff):
                line = filtered_diff[index + i]
                if line.startswith('+'):
                    stdscr.addstr(i, 0, line, curses.color_pair(2) | curses.A_BOLD)  # Vert
                elif line.startswith('-'):
                    stdscr.addstr(i, 0, line, curses.color_pair(1) | curses.A_BOLD)  # Rouge
                else:
                    stdscr.addstr(i, 0, line)
            else:
                break
        
        if len(filtered_diff) > max_lines:
            stdscr.addstr(curses.LINES - 1, 0, f"Press q to quit | Diff: {index / (len(filtered_diff)- max_lines) * 100:.2f}%", curses.A_REVERSE)
        else:
            stdscr.addstr(curses.LINES - 1, 0, "Press q to quit", curses.A_REVERSE)

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_DOWN and index + max_lines < len(filtered_diff):
            index += 1
        elif key == curses.KEY_UP and index > 0:
            index -= 1
        elif key == ord('q'):
            break

if __name__ == '__main__':
    curses.wrapper(main)
