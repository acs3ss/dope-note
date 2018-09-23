import RAKE
import re
from tornado import ioloop, httpclient
import argparse

def handle_request(response):
    if response.code == 200:
        keywords.append(url_dict[response.effective_url.lower()])
    global i
    i -= 1
    if i == 0:
        ioloop.IOLoop.instance().stop()

# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument(dest='filename', help='name of the text file containing parsed subtitles')
parser.add_argument('-n', dest='num_keywords', type=int, default=10, help='number of keywords to extract', )
args = parser.parse_args()
# TODO also pass desired num keywords


with open(args.filename) as f:
    data = f.read()

Rake = RAKE.Rake("SmartStopList.txt")
out = Rake.run(data, minFrequency=2)

url_dict = {}  # dictionary to match url -> (phrases, freq)

keywords = []
urls = []
batch_num = 0
batch_size = args.num_keywords * 2 
i = 0

while len(keywords) < args.num_keywords:
    for phrase, freq in out[batch_size*batch_num:batch_size*(batch_num+1)]:
        urlified = re.sub(" ", "_", phrase)
        url = "https://en.wikipedia.org/wiki/" + urlified
        urls.append(url)
        url_dict[url] = (phrase, freq)

    http_client = httpclient.AsyncHTTPClient()
    for url in urls:
        i += 1
        http_client.fetch(url.strip(), handle_request, method='HEAD')
    
    ioloop.IOLoop.instance().start()
    
    batch_num += 1
    urls = []


keywords.sort(key=lambda entry: entry[1], reverse=True)  # sort by descending relevance
keywords = keywords[:args.num_keywords]  # we may have added more than we needed due to batching. Keep only how many we wanted

print([entry[0] for entry in keywords])

# RAKE - https://github.com/fabianvf/python-rake

