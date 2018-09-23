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
    data = filename

    Rake = RAKE.Rake(stoplist)  # use a stoplist to exclude common words
    out = Rake.run(data, minFrequency=2)  # use RAKE library to find relevant key phrases

    url_dict = {}  # dictionary to match url -> (phrases, relevance)

    keywords = []
    for phrase, relevance in out:
        if len(keywords) >= num_keywords:
            break

        urlified = re.sub(" ", "_", phrase)
        url = "https://en.wikipedia.org/wiki/" + urlified  # convert to Wikipedia url
        url_dict[url] = (phrase, relevance)  # add to dict to allow phrase to later be identified by URL
        request = requests.get(url)
        if request.status_code == 200:
            keywords.append((phrase, relevance))

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
        # bash_command = "googler -l 'en' --json -n 1 -w " + url + ' "' + phrase + '"'
        print(bash_command)
        process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        related_links.append(output)
    return related_links


def get_video_info(url, num_keywords=5, stoplist="SmartStopList.txt", resources="resources.txt"):
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

    links = [get_resources(phrase[0], wanted_resources) for phrase in keywords]

    os.remove(xml_filename)

    data = {}
    data['title'] = title
    data['resources'] = links
    data['transcription'] = transcript
    data['keywords'] = [keyword[0] for keyword in keywords]
    # json_data = json.dumps(data)

    return(data)
