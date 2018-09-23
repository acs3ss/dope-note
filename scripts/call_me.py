from video_analyzer.module import *
import os
import argparse
import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict


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
args = parser.parse_args()

xml_filename = download_subtitles(args.url)
data = parse_xml(xml_filename)
keywords = get_keywords(data, args.num_keywords, args.stoplist)

os.remove(xml_filename)

print(keywords)

