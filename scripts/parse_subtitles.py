#!usr/bin/env python3

import re
import argparse

def getText(filename):
    to_ignore = re.compile(r"\d|$")
    to_remove = re.compile(r"<.*?>")
    with open(filename) as f:
        content = []
        for line in f:
            if to_ignore.match(line):
                continue  # ignore line if blank, time, or index

            stripped = re.sub(to_remove, "", line)  # replace all font coloring, bolding, etc
            stripped = stripped.strip()
            print("LINE:", line)
            print("STRIPPED:", stripped)
            print("------------------")
            content.append(stripped) 
    return " ".join(content)


parser = argparse.ArgumentParser()
parser.add_argument(dest='filename', help='name of the subtitle file')
args = parser.parse_args()

print(getText(args.filename))


