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

def get_word_transcription(word):
    """
    input:  word to search transcription for
    return: filename to jpeg file
    """

    transcription=""

    # get html page
    fp = urllib.request.urlopen(TRANSCRIPTION_REQUEST_STRING.format(word))
    html_page = fp.read().decode("utf8")
    fp.close()

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_page, 'html.parser')
    translation = soup.find(id='us_tr_sound').span.text

    from PIL import Image, ImageDraw, ImageFont
    fn="{}.jpg".format(word)
    # img = Image.new('RGB', (100, 30), color = (73, 109, 137))
    img = Image.new('RGB', TRANSCRIPTION_PICTURE_DIMENSIONS, color = (0, 0, 0))
    # fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', 15)
    fnt = ImageFont.truetype('/usr/share/fonts/adobe-source-code-pro/SourceCodePro-Regular.otf', 17)
    d = ImageDraw.Draw(img)
    d.text((10,10), word + translation, font=fnt, fill=(255,255,255))
    img.save(fn)

    return(fn)
