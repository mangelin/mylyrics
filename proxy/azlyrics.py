from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import requests, re

from .lyrics import LyricsRetriverProxy

class AzlyricsProxy(LyricsRetriverProxy):
    def __init__(self):
        self._name = "AZLyrics"

    def get_artist_page(self, artist:str):
        r = requests.get(f"https://search.azlyrics.com/search.php?q={artist}")
        if r.status_code != 200:
            return None

        soup = bs(r.text, "html.parser")
        a_string = soup.find(string=re.compile("Artist result"))
        if not a_string:
            return None

        t = a_string.findNext("table")
        res = t.find(string=re.compile(artist))
        anchor = res.findParent("a")
        return anchor.get("href")

    def get_lyrics(self, artist_page_url:str, song_name:str):
        r = requests.get(artist_page_url)
        if r.status_code != 200:
            return None

        soup = bs(r.text, "html.parser")
        a_song = soup.find(string=re.compile(song_name))
        anchor = a_song.findParent("a")
        song_relative_url = anchor.get("href")
        song_url = urljoin(artist_page_url,song_relative_url)
        r = requests.get(song_url)
        if r.status_code != 200:
            return None

        return r.text