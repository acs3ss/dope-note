import requests
from bs4 import BeautifulSoup
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(dest='url', help='YouTube video url')
args = parser.parse_args()

req = requests.get(args.url)
soup = BeautifulSoup(req.text, "lxml")

print(soup.title.string)
