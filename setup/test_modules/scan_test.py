import sys
sys.path.append("../..")

from setup.modules.list_scan import scanner
from setup.modules.list import listClass
import curses

if __name__ == "__main__":
    liste = listClass(scanner().scan(), 'Liste des appareils sur le réseau', False, True)
    curses.wrapper(liste.executer)