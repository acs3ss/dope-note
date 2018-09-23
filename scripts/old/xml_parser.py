import xml.etree.ElementTree as ET
import pprint
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument(dest='filename', help='XML file to be parsed')
args = parser.parse_args()


tree = ET.parse(args.filename)

root = tree.getroot()

to_remove = re.compile(r"<.*?>")
apos = re.compile(r"&#39;")

results = []
for child in root:
    cleaned = re.sub(to_remove, "", child.text)
    more_cleaned = re.sub(apos, "'", cleaned)
    results.append(more_cleaned)

output = " ".join(results)

print(output)
