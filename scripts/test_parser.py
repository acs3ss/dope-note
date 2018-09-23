#!/usr/bin/env python3

import json
import argparse
import re
import urllib.parse, urllib.request
import os

def download_subtitles(video):
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
        for ct in caption_tracks:
            filename = "../downloads/" + id + '_' + ct['languageCode']
            urllib.request.urlretrieve(ct['baseUrl'], filename)
    except:
        pass

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
            content.append(stripped)
    return " ".join(content)


# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument(dest='url', help='url of the video to be analyzed')
args = parser.parse_args()

filename = download_subtitles(args.url)

paragraph = getText(filename)

print(paragraph)
