import subprocess
import argparse
import requests
import re
import json

def get_resources(phrase, urls):
    related_links = []
    added = re.sub(r" ", "+", phrase)
    anded = re.sub(r" ", "&20", phrase)
    # bashCommand = "googler -l 'en' --json -n 1 -w " + url + ' "' + phrase + '"'
    # bashCommand = "ddgr -r 'us-en' --json -n 1 -w " + url + ' "' + phrase + '"'
    # process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    # output, error = process.communicate()
    # related_links.append(output)
    # TODO compare top few links from each site, use fuzzywuzzy to return best matches

    related_links.append("https://en.wikipedia.org/w/index.php?search=" + added + "&title=Special%3ASearch&go=Go")
    related_links.append("https://www.youtube.com/results?search_query=" + added)
    related_links.append("https://www.khanacademy.org/search?referer=%2F&page_search_query=" + added)
    related_links.append("https://www.merriam-webster.com/dictionary/" + anded)
    related_links.append("https://stackexchange.com/search?q=" + added)
   
    true_links = []
    for link in related_links:
        request = requests.get(link)
        if request.status_code == 200:
            true_links.append(link)
    return {phrase: true_links}


urls = [
    "khanacademy.org",
    "wikpedia.org",
    "stackexchange.com",
    "merriam-webster.com",
    "youtube.com"
]

# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument(dest='filename', help='name of the text file containing (keyword, relevance) tuples')
args = parser.parse_args()


with open(args.filename) as f:
    data = f.read().splitlines()

resources = {'phrases': [get_resources(phrase, urls) for phrase in data]}

with open('final-json.txt', 'w') as outfile:
    json.dump(resources, outfile)
