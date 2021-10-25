from unittest.mock import MagicMock, patch
from unittest import TestCase
from ..src.lyrics import ProxyLyricsFactory


class ProxyFactoryTestCase(TestCase):
    def setUp(self):
        self.factory = ProxyLyricsFactory()
        self.expected_azlyrics = "AZ"
        self.expected_elyrics = "EZ"
        

    @patch("app.src.lyrics.ElyricsProxy")
    @patch("app.src.lyrics.AzlyricsProxy")
    def test_proxy_factory(self, mock_azlyrics, mock_elyrics):
        mock_azlyrics.get_song = MagicMock(return_value=self.expected_azlyrics)
        mock_elyrics.get_song = MagicMock(return_value=self.expected_elyrics)

        res_az = self.factory.create_proxy("azlyrics")
        self.assertEqual(res_az.get_song(), self.expected_azlyrics)

        res_el = self.factory.create_proxy("elyrics")
        self.assertEqual(res_el.get_song(), self.expected_elyrics)
