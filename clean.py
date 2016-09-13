import urllib2
import re
from bs4 import BeautifulSoup

def htmlToText(url):
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)
    # text = re.sub("[^a-zA-Z0-9\ ]+", "", text) 
    return text.encode('utf-8')
                                                                    
