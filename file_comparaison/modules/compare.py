import curses
from difflib import unified_diff
import json
from os import listdir
from time import strptime
from sys import path
path.append("../..")
from setup.modules.save import set_save

class compareClass:
    def __init__(self) -> None:
        pass

    def read_files(self, device, backup_number, setup_file = "./data/setup_file.json", backup_file = "."):
        
        try:
            backup_location = json.load(open(setup_file, "r"))['backup_location']
            self.devices_list = json.load(open(setup_file, "r"))['devices_list_location']
            list_files = listdir(f"{backup_file}/{backup_location}/{device}")
            list_files = [f"{backup_file}/{backup_location}/{device}/{file}" for file in list_files if file.endswith(".ios")]
            list_files = [file.split('/')[-1] for file in list_files if file.split("/")[-1] != "00-00-00"]
        
            def get_date(filename):
                return strptime(filename[:-4], "%Y-%m-%d-%H-%M-%S")

            sorted_files = sorted(list_files, key=get_date, reverse=True)
            with open(f"{backup_file}/{backup_location}/{device}/{sorted_files[0]}", "r") as f:
                self.f1 = f.read()
            with open(f"{backup_file}/{backup_location}/{device}/{sorted_files[backup_number]}", "r") as f:
                self.f2 = f.read()
            self.backup_selected = f"{backup_file}/{backup_location}/{device}/{sorted_files[backup_number]}"
            curses.wrapper(self.main)
        except FileNotFoundError:
            return None, None

    def main(self, stdscr):
        if curses.has_colors():
            curses.start_color()
            curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

        curses.curs_set(0)  
        stdscr.clear()

        if self.f1 is None or self.f2 is None:
            print("File not found")
            stdscr.addstr("File not found\n")
            stdscr.refresh()
            stdscr.getch()
            return

        diff = unified_diff(self.f1.splitlines(), self.f2.splitlines(), n=20)
        diff_lines = list(diff)[3:]
        filtered_diff = [line for line in diff_lines if not line.startswith("@@")]

        if len(filtered_diff) == 0:
            filtered_diff = self.f1.splitlines()

        index = 0
        max_lines = curses.LINES - 1
        while True:
            stdscr.clear()
            for i in range(max_lines):
                if index + i < len(filtered_diff):
                    line = filtered_diff[index + i]
                    if line.startswith('+'):
                        stdscr.addstr(i, 0, line, curses.color_pair(2) | curses.A_BOLD) # +
                    elif line.startswith('-'):
                        stdscr.addstr(i, 0, line, curses.color_pair(1) | curses.A_BOLD) # -
                    else:
                        stdscr.addstr(i, 0, line)
                else:
                    break
            
            if len(filtered_diff) > max_lines:
                stdscr.addstr(curses.LINES - 1, 0, f"Press q to quit | Press u to upload | Diff: {index / (len(filtered_diff)- max_lines) * 100:.2f}%", curses.A_REVERSE)
            else:
                stdscr.addstr(curses.LINES - 1, 0, "Press q to quit | Press u to upload", curses.A_REVERSE)

            stdscr.refresh()
            key = stdscr.getch()

            if key == curses.KEY_DOWN and index + max_lines < len(filtered_diff):
                index += 1
            elif key == curses.KEY_UP and index > 0:
                index -= 1
            elif key == ord('u'):
                set_save(self.backup_selected, self.devices_list)
                break
            elif key == ord('q'):
                self.f1 = None
                self.f2 = None
                break
