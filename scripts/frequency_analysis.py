from collections import Counter
import argparse
import pprint

parser = argparse.ArgumentParser()
parser.add_argument(dest='filename', help='XML file to be parsed')
args = parser.parse_args()

with open(args.filename) as f:
    data = f.read()

words = Counter(data.split())

for word, value in words.most_common(): 
    print(word, value)

