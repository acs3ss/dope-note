import subprocess


def get_resources(phrase, urls)
    related_links = []
    for url in urls:
        bashCommand = "ddgr -r 'us-en' --json -n 1 -w " + url + ' "' + phrase + '"'
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        related_links.append(output[0])
        # TODO compare top few links from each site, use fuzzywuzzy to return best matches

    return related_links


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
    data = f.read()

phrases = data[:][0]
resouces = [get_links(phrase, urls) for phrase in phrases]

print(resources)
