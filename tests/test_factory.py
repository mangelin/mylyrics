from unittest.mock import MagicMock, patch
from unittest import TestCase
from proxy import ProxyLyricsFactory
from proxy.abstractLyrics import AbstractLyricsRetriverProxy
from proxy.azlyrics import AzlyricsProxy
from proxy.elyrics import ElyricsProxy

from tests import fake

class ProxyFactoryTestCase(TestCase):
    def setUp(self):
        self.factory = ProxyLyricsFactory()

    def test_proxy_factory(self):
        
        res_az = self.factory.create_proxy("azlyrics")
        self.assertTrue(isinstance(res_az, AzlyricsProxy))

        res_el = self.factory.create_proxy("elyrics")
        self.assertTrue(isinstance(res_el, ElyricsProxy))


class TestAbstractProxy(TestCase, AbstractLyricsRetriverProxy):
    def setUp(self):
        self.to_txt_ret = fake.text()
        self.get_lyrics_ret = fake.text()
        self.get_lyrics_url_ret = fake.url()
        self.get_artist_page_ret = fake.url()
        self.outputs = {'txt' : self.to_txt}

    def get_artist_page(self, artist:str):
        return self.get_artist_page_ret

    def get_lyrics_url(self, artist_page_url:str, song_name:str):
        return self.get_lyrics_url_ret
    
    def retrive_lyrics(self, lyrics:str):
        return self.get_lyrics_ret

    def to_txt(self, lyrics:str):
        return self.to_txt_ret

    def test_behaviour_ok(self):
        res = self.get_lyrics('foo','bar')
        self.assertEqual(res, f"{self.to_txt_ret}\nProvided by undefined")

    def test_behaviour_ko_artist_page(self):
        self.get_artist_page_ret = None

        self.assertRaises(ValueError, lambda: self.get_lyrics('foo','bar'))

    def test_behaviour_ko_lyrics(self):
        self.get_lyrics_ret = None

        self.assertRaises(ValueError, lambda: self.get_lyrics('foo','bar'))


