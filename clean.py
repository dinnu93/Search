import urllib2
import re
from bs4 import BeautifulSoup

def htmlToText(url):
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
        # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = ' '.join(chunk for chunk in chunks if chunk)
    text = re.sub("[^a-zA-Z0-9\ ]+", "", text)
    return text
                                                                    
