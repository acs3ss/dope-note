# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import argparse

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
sentiment = client.analyze_sentiment(document=document).document_sentiment

print('Text: {}'.format(text))
print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))
