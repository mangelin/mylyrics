import re
from urllib.parse import urljoin

import config
import requests
from bs4 import BeautifulSoup as bs

from .abstractLyrics import AbstractLyricsRetriverProxy
from .helpers import helper_post_form, helper_retrive_url


# Helpers function
def _locate_string_value(soup, string_value):

    search_string = string_value.split(' ')[0]

    a_string = soup.find("b",string=re.compile(search_string))
    if not a_string:
        return None

    return a_string.parent['href'] if a_string.parent else None

def _get_song_relative_url(soup, song_name:str):
    song_label = soup.find(string=re.compile(f"{song_name.title()}", re.IGNORECASE))
    if not song_label:
        return None
        
    return song_label.parent['href'] if song_label.parent else None
    
# ELyrics concreate proxy
class ElyricsProxy(AbstractLyricsRetriverProxy):
    def __init__(self):
        super().__init__()
        self._name = config.ELYRICS_PROXY

    def get_artist_page_url(self, artist:str)->str:
        r = helper_post_form(config.ELYRICS_SEARCH_URL,{'q':artist})
        if not r:
            return None


        soup = bs(r, "html.parser")
        a_string = _locate_string_value(soup, artist.upper())
        if not a_string:
            return None

        return urljoin(config.ELYRICS_BASE_URL,a_string)

    def get_lyrics_url(self, artist_page_url:str, song_name:str)->str:
        r = helper_retrive_url(artist_page_url)
        if not r:
            return None

        soup = bs(r, "html.parser")

        song_relative_url = _get_song_relative_url(soup, song_name.title())
        if not song_relative_url:
            return None

        song_url = urljoin(artist_page_url,song_relative_url)

        return song_url

    def fetch_lyric_content(self, lyrics_url:str)->str:
        return helper_retrive_url(lyrics_url) # pragma: no cover

    def to_txt(self, lyrics):
        soup = bs(lyrics, "html.parser")
        div_lyrics = soup.find(attrs={"id":"inlyr"})
        return div_lyrics.text
