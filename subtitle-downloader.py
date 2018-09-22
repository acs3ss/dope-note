#!/usr/bin/python3

import re
import urllib.parse, urllib.request

def download_subtitles(video):
    id = retrieve_id(video)
    url = "https://www.youtube.com/api/timedtext?lang=en&fmt=vtt&name=&v={0}".format(id)
    urllib.request.urlretrieve(url, id)

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


download_subtitles("https://www.youtube.com/watch?v=jNQXAC9IVRw")
