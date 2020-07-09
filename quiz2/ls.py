import sys
import os
from os.path import expanduser

COL_WIDTH = 4
DELIMITER = "	"


class PrintStyle(object):
    BOLD = '\033[1m'
    END = '\033[0m'


def print_list(items):
    print(DELIMITER.join(items))


def print_in_col(items, col_num):
    for i in range(0, len(items), col_num):
        end_idx = i + col_num
        print_list(items[i:end_idx])


def format_entry(entry, is_folder=False):
    txt = None
    if is_folder:
        txt = f"{PrintStyle.BOLD}{entry}{PrintStyle.END}"
    else:
        txt = entry
    return txt


def parse_raw_path(src):
    if src.startswith("~/") or src == "~":
        paths = src.split("/")
        paths[0] = expanduser("~")
        src = "/".join(paths)
    return src


def show_folder_content(folder_path, is_recursive=False, is_print_path=False):
    sub_folders = []

    if is_print_path:
        print(f"\n{folder_path}:")

    fmt_entries = []
    for index, entry in enumerate(sorted(os.listdir(folder_path))):
        if entry.startswith("."):
            continue

        is_folder = False
        full_path = f"{folder_path}/{entry}"
        if os.path.isdir(full_path):
            sub_folders.append(full_path)
            is_folder = True

        fmt_entries.append(format_entry(entry, is_folder))

    print_in_col(fmt_entries, COL_WIDTH)

    if is_recursive:
        for sub in sub_folders:
            show_folder_content(sub, is_recursive=True, is_print_path=True)


if __name__ == "__main__":
    sys_args = sys.argv[1:]
    passed_args = [s for s in sys_args if s.startswith("-")]

    is_recursive = False
    if passed_args:
        if len(passed_args) > 1:
            print(f"ERROR: Only 1 parameter accepted")
            sys.exit(1)

        arg = passed_args.pop()
        sys_args.pop(sys_args.index(arg))
        if arg:
            if arg != "-R":
                print(f"ERROR: Invalid argument. Only -R accepted")
                sys.exit(1)
            else:
                is_recursive = True

    folders = []
    files = []

    for entry in sys_args:
        entry = parse_raw_path(entry)
        if os.path.isdir(entry):
            folders.append(entry)
        elif os.path.isfile(entry):
            files.append(entry)
        else:
            print(f"ls: {entry}: No such file or directory")

    is_print_path = False
    if files:
        is_print_path = True
        print_list(files)

    for folder in folders:
        show_folder_content(
            folder,
            is_recursive=is_recursive,
            is_print_path=is_print_path
        )
