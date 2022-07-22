import os
import re
import argparse

from matplotlib.pyplot import get


def get_arg_file():
    parser = argparse.ArgumentParser(
        description='Add named anchors to the specify markdown file.')
    parser.add_argument("-f", help="Specify the file to edit.")
    args = parser.parse_args()
    return args.f


def file_inexistent():
    print("This file doesn't exist or maybe you forgot the -f option")


def file_bad_extension():
    print("I'm sorry, but this script is only for *.md files")


def add_named_anchor(file_path):
    with open(file_path) as f:
        file_text = f.read()
        targets = re.findall(r"\(#.*\)", file_text)

        with open(file_path) as f:
            file_lines = f.readlines()

        for target in targets:
            formated_target = f"# {target[2:-1].replace('-', ' ')}\n"

            for line_index in range(len(file_lines)):
                line_lower = file_lines[line_index].lower()
                if formated_target in line_lower:
                    file_lines[line_index] = file_lines[line_index][:-1] + \
                        f"<a name={target[2:-1]}></a>"

        with open(file_path, "w") as f:
            f.writelines(file_lines)
            print(f'{len(targets)} links has been updated with named anchors.')


if __name__ == "__main__":
    file_path = get_arg_file()

    for _, __, files in os.walk("."):
        if file_path not in files:
            file_inexistent()
        elif file_path.endswith(".md"):
            add_named_anchor(file_path)
        else:
            file_bad_extension()
