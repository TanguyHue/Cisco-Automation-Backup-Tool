import sys
sys.path.append("../..")

from setup.modules.list_scan import scanner
from setup.modules.list import ListeAvecCases
import curses

if __name__ == "__main__":
    liste = ListeAvecCases(scanner().scan(), False, True)
    curses.wrapper(liste.executer)