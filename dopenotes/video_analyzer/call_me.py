import os
import argparse
import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict
import json
import requests
from bs4 import BeautifulSoup
import subprocess
import json
import re
import urllib.parse, urllib.request
import xml.etree.ElementTree as ET
import RAKE
from tornado import ioloop, httpclient

thread_count = []

def download_subtitles(video):
    ''' @param video: YouTube url
        @return: XML of subtitle transcript
    '''
    id = retrieve_id(video)

    # Lots of the following taken from you-get
    req = urllib.request.Request(video)

    response = urllib.request.urlopen(req)
    data = response.read()

    # Handle HTTP compression for gzip and deflate (zlib)
    content_encoding = response.getheader('Content-Encoding')
    if content_encoding == 'gzip':
        data = ungzip(data)
    elif content_encoding == 'deflate':
        data = undeflate(data)

    # Decode the response body
    match = re.search(r'charset=([\w-]+)', response.getheader('Content-Type'))
    if match:
        data = data.decode(match.group(1))
    else:
        data = data.decode('utf-8', 'ignore')

    video_page = data
    ytplayer_config = json.loads(re.search('ytplayer.config\s*=\s*([^\n]+?});', video_page).group(1))
    try:
        caption_tracks = json.loads(ytplayer_config['args']['player_response'])['captions']['playerCaptionsTracklistRenderer']['captionTracks']
        filename = False
        for ct in caption_tracks:
            if ct['languageCode'] == 'en':
                filename = id + '_' + ct['languageCode']
                urllib.request.urlretrieve(ct['baseUrl'], filename)
                break
        if not filename:
            filename = id + '_' + caption_tracks[0]['languageCode']
            urllib.request.urlretrieve(caption_tracks[0]['baseUrl'], filename)
    except:
        return None

    return filename


def retrieve_id(url):
    # Adopted from you-get
    match = re.search(r'(?:youtube\.com/(?:embed|v|watch)|youtu\.be)/([^/?]+)', url)
    if match:
        return match.group(1)
    else:
        try:
            return urllib.parse.parse_qs(urllib.parse.urlparse(url).query)['v'][0]
        except:
            return None


def get_video_title(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "lxml")
    return soup.title.string


def parse_xml(filename):
    ''' @param filename: path to the xml file to be parsed
        @return: string of all text from xml file in paragraph form
    '''
    tree = ET.parse(filename)

    root = tree.getroot()

    to_remove = re.compile(r"<.*?>")
    apos = re.compile(r"&#39;")

    results = []
    for child in root:
        cleaned = re.sub(to_remove, "", child.text)
        more_cleaned = re.sub(apos, "'", cleaned)
        results.append(more_cleaned)

    output = " ".join(results)

    return output


def get_keywords(filename, num_keywords, stoplist):
    ''' @param filename: path to the text file containing speech
        @param num_keywords: number of keywords to extract
        @param stoplist: path to stoplist of common words to be excluded
        @return: list of (keyword, relevance) sorted by descreasing relevance
    '''
    def handle_request(response, i):
        if response.code == 200:  # if valid url, append to keywords list
            keywords.append(url_dict[response.effective_url.lower()])
        thread_count[i] -= 1
        if thread_count[i] == 0:
            ioloop.IOLoop.instance().stop()  # once all threads are done, stop the instance

    def worker(ws, loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(ws.start())

    if __name__ == '__main__':
        ws = Server()
        loop = asyncio.new_event_loop()
        p = threading.Thread(target=worker, args=(ws, loop,))
        p.start()

#    with open(filename) as f:
#        data = f.read()
    data = filename

    Rake = RAKE.Rake(stoplist)  # use a stoplist to exclude common words
    out = Rake.run(data, minFrequency=2)  # use RAKE library to find relevant key phrases

    url_dict = {}  # dictionary to match url -> (phrases, relevance)

    keywords = []
    urls = []
    batch_num = 0
    batch_size = num_keywords * 2  # number of threads sent out at once
    while len(keywords) < num_keywords:
        for phrase, relevance in out[batch_size*batch_num:batch_size*(batch_num+1)]:
            urlified = re.sub(" ", "_", phrase)
            url = "https://en.wikipedia.org/wiki/" + urlified  # convert to Wikipedia url
            urls.append(url)
            url_dict[url] = (phrase, relevance)  # add to dict to allow phrase to later be identified by URL

        http_client = httpclient.AsyncHTTPClient()
        thread_count.append(0)
        for url in urls:
            thread_count[batch_num] += 1
            http_client.fetch(url.strip(), handle_request(batch_num), method='HEAD')  # check if Wikipedia page exists for phrase

        ioloop.IOLoop.instance().start()

        batch_num += 1
        urls = []

    keywords.sort(key=lambda entry: entry[1], reverse=True)  # sort by descending relevance
    keywords = keywords[:num_keywords]  # we may have added more than we needed due to batching. Keep only how many we wanted

    return keywords


def get_resources(phrase, urls):
    ''' @param phrase: phrase to be searched for
        @param urls: websites to search for the phrase
        @return: json objects from top ddgr search results
    '''
    related_links = []
    for url in urls:
        bash_command = "ddgr -r 'us-en' --json -n 1 -w " + url + ' "' + phrase + '"'
        print(bash_command)
        process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        related_links.append(output[0])
    return related_links


def get_video_info(url, num_keywords=10, stoplist="SmartStopList.txt", resources="resources.txt"):
    dependencies = [
        'you-get>=0.4.1099',
        'python-rake>=1.4.5'
    ]

    # here, if a dependency is not met, a DistributionNotFound or VersionConflict
    # exception is thrown.
    pkg_resources.require(dependencies)

    wanted_resources = open(resources).read().splitlines()  # parse resources file into list

    try:
        xml_filename = download_subtitles(url)
        if not xml_filename:
            raise ValueError('This video does not have subtitles')
    except ValueError as err:
        print(err.args)
        exit(1)

    title = get_video_title(url)
    transcript = parse_xml(xml_filename)
    keywords = get_keywords(transcript, num_keywords, stoplist)

    links = [(phrase[0], get_resources(phrase[0], wanted_resources)) for phrase in keywords]

    os.remove(xml_filename)

    data = {}
    data['title'] = title
    dopen(args.resources).read().splitlines()  # parse resources file into listata['resources'] = links
    data['transcript'] = transcript
    data['keywords'] = [keyword[0] for keyword in keywords]
    json_data = json.dumps(data)

    return(json_data)
