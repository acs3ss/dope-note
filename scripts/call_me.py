from video_analyzer.module import *
import os
import argparse
import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict
import json

def get_video_info(url):
    dependencies = [
        'you-get>=0.4.1099',
        'python-rake>=1.4.5'
    ]
    
    # here, if a dependency is not met, a DistributionNotFound or VersionConflict
    # exception is thrown. 
    pkg_resources.require(dependencies)
    
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='url', help='YouTube video to be parsed')
    parser.add_argument('-n', dest='num_keywords', type=int, default=10, help='number of keywords to extract')
    parser.add_argument('--stoplist', dest='stoplist', default="SmartStopList.txt", help='path to stoplist of common words to be excluded')
    parser.add_argument('--resources', dest='resources', default="resources.txt", help='path to list of  resources to search')
    args = parser.parse_args()
    
    wanted_resources = open(args.resources).read().splitlines()  # parse resources file into list
    
    try:
        xml_filename = download_subtitles(args.url)
        if not xml_filename:
            raise ValueError('This video does not have subtitles')
    except ValueError as err:
        print(err.args)
        exit(1)
    
    title = get_video_title(args.url)
    transcript = parse_xml(xml_filename)
    keywords = get_keywords(transcript, args.num_keywords, args.stoplist)
    
    # resources = [(phrase[0], get_resources(phrase[0], wanted_resources)) for phrase in keywords]
    
    os.remove(xml_filename)
    
    data = {}
    data['title'] = title
    data['resources'] = resources
    data['transcript'] = transcript
    data['keywords'] = [keyword[0] for keyword in keywords]
    json_data = json.dumps(data)
    
    return(json_data)
