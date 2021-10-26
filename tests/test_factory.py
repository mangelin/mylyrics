from unittest.mock import MagicMock, patch
from unittest import TestCase
from proxy import ProxyLyricsFactory
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


class AZLyricsTestCase(TestCase):
    def setUp(self):
        self.expected_lyrics = fake.text()
        self.expected_artist = fake.name()
        self.expected_songname = fake.name()

        self.proxy_name = "azlyrics"
        self.factory = ProxyLyricsFactory()
        self.proxy = self.factory.create_proxy(self.proxy_name)

    def test_proxy_name(self):
        self.assertEqual(self.proxy.name, "AZLyrics")

    @patch("proxy.azlyrics.AzlyricsProxy.get_song")
    def test_get_song(self,mock_get_song):
        mock_get_song.return_value = self.expected_lyrics
        
        p = self.factory.create_proxy(self.proxy_name)

        self.assertEqual(p.get_song(self.expected_artist,self.expected_songname), self.expected_lyrics)