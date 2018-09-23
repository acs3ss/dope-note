# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import argparse
import pprint

# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument(dest='filename', help='name of the text file containing parsed subtitles')
args = parser.parse_args()

with open(args.filename) as f:
    subtitles = f.read()

# Instantiates a client
client = language.LanguageServiceClient()

# The text to analyze
text = subtitles
document = types.Document(
    content=text,
    type=enums.Document.Type.PLAIN_TEXT)

# Detects the sentiment of the text
categories = client.classify_text(document=document).categories
entities = client.analyze_entities(document=document).entities

for category in categories:
    print(u'=' * 20)
    print(u'{:<16}: {}'.format('name', category.name))
    print(u'{:<16}: {}'.format('confidence', category.confidence))

for entity in entities:
    if entity.salience > 0.05:
        pprint.pprint(entity)

# print('Text: {}'.format(text))
# print('Sentiment: {}, {}'.format(sentiment, sentiment.magnitude))
