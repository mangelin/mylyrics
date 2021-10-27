from unittest.mock import patch, Mock
from unittest import TestCase
from tests import fake

from proxy.helpers import helper_post_form, helper_retrive_url

class TestHelpersTestCase(TestCase):
    def setUp(self) -> None:
        self.mock_ret_ok = Mock()
        self.mock_ret_ok.status_code = 200
        self.mock_ret_ok.text = fake.text()

        self.mock_ret_ko = Mock()
        self.mock_ret_ko.status_code = 500
        

    @patch('requests.get')
    def test_helper_retrive_url(self, mock_request):
        mock_request.return_value = self.mock_ret_ok

        ret = helper_retrive_url(fake.url())

        self.assertEqual(ret, self.mock_ret_ok.text)

        mock_request.return_value = self.mock_ret_ko

        ret = helper_retrive_url(fake.url())

        self.assertIsNone(ret)

    @patch('requests.post')
    def test_helper_post_form(self, mock_request):
        mock_request.return_value = self.mock_ret_ok

        ret = helper_post_form(fake.url(), {'q':fake.name()})

        self.assertEqual(ret, self.mock_ret_ok.text)

        mock_request.return_value = self.mock_ret_ko

        ret = helper_post_form(fake.url(), {'q':fake.name()})

        self.assertIsNone(ret)


        
