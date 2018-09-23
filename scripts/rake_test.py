import RAKE
import requests
import re

with open("gabe") as f:
    data = f.read()

Rake = RAKE.Rake("SmartStopList.txt")
out = Rake.run(data, minFrequency=2)

keywords = []

for phrase, freq in out:
    if len(keywords) < 10:
        urlified = re.sub(" ", "_", phrase)
        url = "https://en.wikipedia.org/wiki/" + urlified

        request = requests.get(url)
        if request.status_code == 200:
            keywords.append(phrase)
    else:
        break

print(keywords)

# RAKE - https://github.com/fabianvf/python-rake
