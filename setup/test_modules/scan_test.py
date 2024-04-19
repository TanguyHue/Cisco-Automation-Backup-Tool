import sys
sys.path.append("..")

from modules.list_scan import scanner
from modules.list import ListeAvecCases
import curses

if __name__ == "__main__":
    liste = ListeAvecCases(scanner().scan(), False, True)
    curses.wrapper(liste.executer)