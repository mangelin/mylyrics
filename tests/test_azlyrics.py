from unittest.mock import Mock, patch, MagicMock
from unittest import TestCase
from proxy import ProxyLyricsFactory

import config

from proxy.azlyrics import _locate_anchor

from tests import fake
class AZLyricsTestCase(TestCase):
    def setUp(self):
        self.expected_lyrics = fake.text()
        self.expected_artist = fake.name()
        self.expected_songname = fake.name()
        self.expected_artist_link = fake.url()

        self.proxy_name = config.AZLYRICS_PROXY.lower()
        self.factory = ProxyLyricsFactory()
        self.proxy = self.factory.create_proxy(self.proxy_name)

        self.artist_page_url = fake.url()
        self.song_relative_url = fake.uri_path()

        self.mock_soup = Mock()
        self.mock_soup.find = MagicMock(return_value=None)
        self.mock_soup.findNext = MagicMock(return_value=None)

    def test_proxy_name(self):
        self.assertEqual(self.proxy.name, config.AZLYRICS_PROXY)

    @patch("proxy.azlyrics.AzlyricsProxy.get_lyrics")
    def test_get_lyrics(self,mock_get_lyrics):
        mock_get_lyrics.return_value = self.expected_lyrics
        
        p = self.factory.create_proxy(self.proxy_name)

        self.assertEqual(p.get_lyrics(self.expected_artist,self.expected_songname), self.expected_lyrics)

    @patch("requests.get")
    @patch("proxy.azlyrics.bs")
    @patch("proxy.azlyrics._locate_anchor")
    def test_get_artist_page_ok(self, 
            mock_laa,
            mock_bs,
            mock_requests):

        self.mock_soup.find.return_value = True
        self.mock_soup.findNext.return_value = True
        mock_bs.return_value = self.mock_soup

        req_mock = MagicMock()
        req_mock.status_code = 200
        req_mock.text = f"<html><body><p>{fake.text()}</p></body></html>"

        mock_requests.return_value = req_mock
        mock_laa.return_value = self.expected_artist_link
        
        res = self.proxy.get_artist_page_url('foo')

        self.assertEqual(res, self.expected_artist_link)

    @patch("requests.get")
    def test_get_artist_page_ko_request(self, mock_requests):

        req_mock = MagicMock()
        req_mock.status_code = 404
        
        mock_requests.return_value = req_mock
        
        res = self.proxy.get_artist_page_url('foo')

        self.assertIsNone(res)

    @patch("proxy.azlyrics.bs")
    @patch("requests.get")
    def test_get_artist_page_ko_locate_string_value(self, mock_requests, mock_bs):

        req_mock = MagicMock()
        req_mock.status_code = 200
        req_mock.text = f"<html><body><p>{fake.text()}</p></body></html>"
        
        mock_requests.return_value = req_mock
        mock_bs.return_value = self.mock_soup
        
        res = self.proxy.get_artist_page_url('foo')

        self.assertIsNone(res)

    @patch("proxy.azlyrics.bs")
    @patch("requests.get")
    def test_get_artist_page_ko_locate_artist_table(self, mock_requests, mock_bs):

        req_mock = MagicMock()
        req_mock.status_code = 200
        req_mock.text = f"<html><body><p>{fake.text()}</p></body></html>"
        
        mock_requests.return_value = req_mock
        self.mock_soup.find.return_value = True
        mock_bs.return_value = self.mock_soup

        res = self.proxy.get_artist_page_url('foo')

        self.assertIsNone(res)

    @patch("proxy.azlyrics._locate_anchor")
    @patch("proxy.azlyrics.bs")
    @patch("requests.get")
    def test_get_artist_page_ko_locate_artist_ancor(self, mock_requests, 
        mock_bs,mock_laa):

        req_mock = MagicMock()
        req_mock.status_code = 200
        req_mock.text = f"<html><body><p>{fake.text()}</p></body></html>"
        
        mock_requests.return_value = req_mock
        self.mock_soup.find.return_value = True
        self.mock_soup.findNext.return_value = True
        mock_bs.return_value = self.mock_soup
        mock_laa.return_value = None
        
        res = self.proxy.get_artist_page_url('foo')

        self.assertIsNone(res)


    @patch("proxy.azlyrics.helper_retrive_url")
    def test_get_lyrics_url_ko(self, mock_retrive_url):
        mock_retrive_url.return_value = None

        res = self.proxy.get_lyrics_url('foo','bar')

        self.assertIsNone(res)

    @patch("proxy.azlyrics._locate_anchor")
    @patch("proxy.azlyrics.helper_retrive_url")
    def test_get_lyrics_url(self, mock_retrive_url, mock_locate_anchor):
        mock_retrive_url.return_value = f"<html><body><p>{fake.text()}</p></body></html>"
        mock_locate_anchor.return_value = self.song_relative_url

        res = self.proxy.get_lyrics_url(self.artist_page_url,'bar')

        self.assertEqual(res, f"{self.artist_page_url}{self.song_relative_url}")

        mock_locate_anchor.return_value = None

        res = self.proxy.get_lyrics_url(self.artist_page_url,'bar')

        self.assertIsNone(res)

    @patch("proxy.azlyrics.bs")
    def test_txt(self, mock_bs):
        mock_soup = Mock()
        mock_div = Mock()
        mock_res = Mock()
        mock_res.text = MagicMock(return_value=self.expected_lyrics)
        mock_div.findNext = MagicMock(return_value=mock_res)
        mock_soup.find = MagicMock(return_value=mock_div)
        mock_bs.return_value = mock_soup

        res = self.proxy.to_txt('foo')

        self.assertTrue(res, self.expected_lyrics)
    
class AZLyricsHelpersTestCase(TestCase):
    def setUp(self) -> None:
        self.mock_soup = Mock()
        self.mock_res = Mock()
        self.uri = fake.uri_path()
    
    def test_locate_anchor_ko(self):
        self.mock_soup.find = MagicMock(return_value=None)

        res = _locate_anchor(self.mock_soup,'foo')

        self.assertIsNone(res)

        self.mock_res.findParent = MagicMock(return_value=None)
        self.mock_soup.find = MagicMock(return_value=self.mock_res)

        res = _locate_anchor(self.mock_soup,'foo')

        self.assertIsNone(res)

    def test_locate_anchor_ok(self):
        self.mock_res.findParent = MagicMock(return_value={'href':self.uri})
        self.mock_soup.find = MagicMock(return_value=self.mock_res)

        res = _locate_anchor(self.mock_soup,'foo')

        self.assertEqual(res, self.uri)
