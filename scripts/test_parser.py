#!/usr/bin/env python3

import argparse
import re
import urllib.parse, urllib.request
import os

def download_subtitles(video):
    video_id = retrieve_id(video)
    url = "https://www.youtube.com/api/timedtext?lang=en&fmt=vtt&name=&v={0}".format(video_id)
    try:
        local_filename, headers = urllib.request.urlretrieve(url, "../downloads/" + video_id)
        file_size = os.path.getsize(local_filename)  # check if file is empty
        if file_size == 0:
            raise ValueError("This video has no subtitles")
    except ValueError as err:
        print(err.args)
        exit(1)  # failure

    return local_filename


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
