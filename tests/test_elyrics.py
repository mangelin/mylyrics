from unittest.mock import Mock, patch, MagicMock
from unittest import TestCase
from proxy import ProxyLyricsFactory
import config

from proxy.elyrics import (
    _locate_string_value, 
    _get_song_relative_url,
)

from tests import fake

class ELyricsProxyTestCase(TestCase):
    def setUp(self) -> None:
        self.expected_lyrics = fake.text()
        self.expected_artist = fake.name()
        self.expected_songname = fake.name()
        self.expected_artist_link = fake.url()

        self.proxy_name = config.ELYRICS_PROXY.lower()
        self.proxy = ProxyLyricsFactory.get(self.proxy_name)

        self.artist_url = fake.uri_path()
        self.song_relative_url = fake.uri_path()
        self.artist_full_url = fake.url()

    
    def test_proxy_name(self):
        self.assertEqual(self.proxy.name, config.ELYRICS_PROXY)

    @patch("proxy.elyrics.helper_post_form")
    @patch("proxy.elyrics._locate_string_value")
    @patch("proxy.elyrics.bs")
    def test_get_artist_page_url_ko(self, mock_bs, mock_lsv, mock_hpf):
        mock_hpf.return_value = None

        res = self.proxy.get_artist_page_url(fake.name())
        self.assertIsNone(res)

        mock_hpf.return_value = fake.url()
        mock_lsv.return_value = None

        res = self.proxy.get_artist_page_url(fake.name())
        self.assertIsNone(res)

    @patch("requests.post")
    def test_get_artist_page_url_request_exception(self, mock_post):
        mock_post.side_effect = Exception
        self.assertRaises(Exception, lambda: self.proxy.get_artist_page_url(fake.name()))

    @patch("proxy.elyrics.helper_post_form")
    @patch("proxy.elyrics._locate_string_value")
    @patch("proxy.elyrics.bs")
    def test_get_artist_page_url_ok(self, mock_bs, mock_lsv, mock_hpf):
        mock_hpf.return_value = fake.url()
        mock_lsv.return_value = self.artist_url

        res = self.proxy.get_artist_page_url(fake.name())
        self.assertEqual(res, f"{config.ELYRICS_BASE_URL}/{self.artist_url}")

    @patch("proxy.elyrics._get_song_relative_url")
    @patch("proxy.elyrics.helper_retrive_url")
    @patch("proxy.elyrics.bs")
    def test_get_lyrics_url_ok(self, mock_bs, mock_hru, mock_gsru):
        mock_bs.return_value = True
        mock_hru.return_value = True
        mock_gsru.return_value = self.song_relative_url

        res = self.proxy.get_lyrics_url(self.artist_full_url, fake.name())
        self.assertEqual(res, f"{self.artist_full_url}{self.song_relative_url}")

    @patch("proxy.elyrics._get_song_relative_url")
    @patch("proxy.elyrics.helper_retrive_url")
    @patch("proxy.elyrics.bs")
    def test_get_lyrics_url_ko(self,mock_bs, mock_hru, mock_gsru):
        mock_hru.return_value = None
        res = self.proxy.get_lyrics_url(self.artist_full_url, fake.name())
        self.assertIsNone(res)

        mock_hru.return_value = True
        mock_gsru.return_value = None
        res = self.proxy.get_lyrics_url(self.artist_full_url, fake.name())
        self.assertIsNone(res)

    @patch("proxy.elyrics.bs")
    def test_to_txt(self, mock_bs):
        fake_txt = fake.text()
        
        mock_div = Mock()
        mock_div.text = fake_txt
        
        mock_soup = Mock()
        mock_soup.find = MagicMock(return_value=mock_div)
        
        mock_bs.return_value = mock_soup

        res = self.proxy.to_txt(fake.text())

        self.assertEqual(res, fake_txt)


class ELyricsProxyHelpersTestCase(TestCase):
    def setUp(self) -> None:
        self.mock_tag_ok = Mock()
        self.mock_tag_ok.parent = Mock()
        self.mock_tag_ok.parent = {'href' : fake.url()}

        self.mock_tag_ko = Mock()
        self.mock_tag_ko.parent = None

        self.mock_soup = Mock()
        self.mock_soup.find = MagicMock(return_value=None)


    def test_locate_string_value_ko(self):

        res = _locate_string_value(self.mock_soup, fake.name())

        self.assertIsNone(res)

        self.mock_soup.find.return_value = self.mock_tag_ko
    
        res = _locate_string_value(self.mock_soup, fake.name())

        self.assertIsNone(res)
    
    def test_locate_string_value_ok(self):

        self.mock_soup.find.return_value = self.mock_tag_ok
        
        res = _locate_string_value(self.mock_soup, fake.name())

        self.assertEqual(res, self.mock_tag_ok.parent['href'])

    def test_get_song_relative_url_ko(self):

        res = _get_song_relative_url(self.mock_soup, fake.name())
        self.assertIsNone(res)

        self.mock_soup.find.return_value = self.mock_tag_ko

        res = _get_song_relative_url(self.mock_soup, fake.name())
        self.assertIsNone(res)

    def test_get_song_relative_url_ok(self):

        self.mock_soup.find.return_value = self.mock_tag_ok

        res = _get_song_relative_url(self.mock_soup, fake.name())

        self.assertEqual(res, self.mock_tag_ok.parent['href'])
    