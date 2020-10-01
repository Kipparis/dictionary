import os
import urllib.request
import urllib.error
import http.client

from .settings import *

def get_word_pronounciation(word):
    """
    input:  word to search pronounciation for
    return: filename to mp3 file
    """
    # TODO: case where there are several words
    fn=f"{word}.mp3"

    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path=os.path.join(base_path, fn)

    url = PRONOUNCIATION_REQUEST_STRING.format(word)
    try:
        urllib.request.urlretrieve(url, path)
    except urllib.error.HTTPError:
        print("'{}' not found at specified url".format(word))
        path=""
    except http.client.InvalidURL:
        print("Can't extract url: '{}'".format(url))
        path=""

    return(path)

def get_word_transcription(phrase):
    """
    input:  phrase to search transcription for
    return: filename to jpeg file
    """
    from bs4 import BeautifulSoup

    translations = []
    for word in phrase.split(" "):
        # get html page
        fp = urllib.request.urlopen(TRANSCRIPTION_REQUEST_STRING.format(word))
        html_page = fp.read().decode("utf8")
        fp.close()

        soup = BeautifulSoup(html_page, 'html.parser')
        entry = soup.find(id='us_tr_sound')
        if entry is not None:
            translations.append(entry.span.text[2:-1])

    return(" ".join(translations))
