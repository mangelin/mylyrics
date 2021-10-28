from unittest.mock import MagicMock, patch
from unittest import TestCase
from io import StringIO

import config
from proxy import ProxyLyricsFactory
from proxy.abstractLyrics import AbstractLyricsRetriverProxy

from tests import fake

class ProxyFactoryTestCase(TestCase):
    def setUp(self):
        self.factory = ProxyLyricsFactory()

    def test_proxy_factory(self):
        for provider in config.providers():
            res = self.factory.create_proxy(provider)
            self.assertIsNotNone(res)

    @patch('proxy.config')
    def test_proxy_factory_exception(self, mock_config):
        mock_config.providers.return_value = [fake.name()]

        self.assertRaises(ValueError, lambda: self.factory.create_proxy(fake.name()))

class TestAbstractProxy(TestCase, AbstractLyricsRetriverProxy):
    def setUp(self):
        self.to_txt_ret = fake.text()
        self.get_lyrics_ret = fake.text()
        self.get_lyrics_url_ret = fake.url()
        self.get_artist_page_ret = fake.url()
        self.outputs = {'txt' : self.to_txt}

    def get_artist_page_url(self, artist:str):
        return self.get_artist_page_ret

    def get_lyrics_url(self, artist_page_url:str, song_name:str):
        return self.get_lyrics_url_ret
    
    def fetch_lyric_content(self, lyrics:str):
        return self.get_lyrics_ret

    def to_txt(self, lyrics:str):
        return self.to_txt_ret

    def test_behaviour_ok(self):
        res = self.get_lyrics('foo','bar')
        self.assertEqual(res, f"{self.to_txt_ret}\nProvided by undefined")

    def test_behaviour_ko_lyrics_url(self):
        self.get_lyrics_url_ret = None

        self.assertRaises(ValueError, lambda: self.get_lyrics('foo','bar'))

    def test_behaviour_ko_artist_page(self):
        self.get_artist_page_ret = None

        self.assertRaises(ValueError, lambda: self.get_lyrics('foo','bar'))

    def test_behaviour_ko_lyrics(self):
        self.get_lyrics_ret = None

        self.assertRaises(ValueError, lambda: self.get_lyrics('foo','bar'))

    def test_format_result(self):
        ret = self._format_result('foo','txt')
        
        self.assertEqual(ret, self.to_txt_ret)

        self.assertRaises(ValueError, lambda: self._format_result('foo','xml'))



