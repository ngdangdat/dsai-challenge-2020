import sys
import os

from os.path import expanduser
home = expanduser("~")


class PrintStyle(object):
    BOLD = '\033[1m'
    END = '\033[0m'


def print_entry(entry, is_folder):
    txt = None
    if is_folder:
        txt = f"{PrintStyle.BOLD}{entry}{PrintStyle.END}"
    else:
        txt = entry
    print(txt, end="	")


def parse_raw_folder(src):
    if src.startswith("~/") or src == "~":
        paths = src.split("/")
        paths[0] = expanduser("~")
        src = "/".join(paths)
    return src


def show_folder_content(folder_path, is_recursive=False, is_sub=False):
    folder_path = parse_raw_folder(folder_path)

    sub_folders = []

    if is_sub:
        print(f"\n{folder_path}:")

    for entry in sorted(os.listdir(folder_path)):
        if entry.startswith("."):
            continue

        is_folder = False
        full_path = f"{folder_path}/{entry}"
        if os.path.isdir(full_path):
            sub_folders.append(full_path)
            is_folder = True
        print_entry(entry, is_folder)

    if is_recursive:
        for sub in sub_folders:
            show_folder_content(sub, True, True)


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
    for entry in sys_args:
        if os.path.isdir(entry):
            folders.append(entry)
        elif os.path.isfile(entry):
            print_entry(entry, False)
        else:
            print(f"ls: {entry}: No such file or directory")

    for folder in folders:
        show_folder_content(folder, is_recursive=is_recursive)
