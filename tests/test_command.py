from unittest.mock import MagicMock, Mock, patch
from unittest import TestCase
from unittest import mock
from management.command import (
    save_to_folder,
    load_from_folder,
    MyLyricsCommand
)
from tests import fake
import pytest

class MyLyricsCommandTestCase(TestCase):
    pass

class MyLyricsCommandHelpersTestCase(TestCase):
    def setUp(self) -> None:
        self.artist = fake.name()
        self.song = fake.name()
        self.lyrics = fake.text()

    @patch("builtins.open")
    def test_load_from_folder_exception(self, mock_open):
        exception_text = fake.name()
        mock_open.side_effect = Exception(exception_text)
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            res = load_from_folder(self.artist, self.song)

        self.assertEqual(pytest_wrapped_e.type, SystemExit)
        self.assertEqual(str(pytest_wrapped_e.value), f"Warning: {exception_text}\n")

    def test_load_from_folder_file_not_found(self):        
        mock_open = mock.mock_open(read_data=self.lyrics)
        mock_open.side_effect = FileNotFoundError
        with mock.patch("builtins.open", mock_open):
            res = load_from_folder(self.artist, self.song)
            self.assertIsNone(res)


    def test_load_from_folder(self):
        mock_open = mock.mock_open(read_data=self.lyrics)
        with mock.patch("builtins.open", mock_open):
            res = load_from_folder(self.artist, self.song)
            self.assertEqual(res, self.lyrics)

    @patch("management.command.Path")
    @patch("builtins.open")
    def test_save_to_folder_exception(self, mock_open, mock_path):
        exception_text = fake.text()
        mock_open.side_effect = Exception(exception_text)
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            save_to_folder(self.artist, self.song, self.lyrics)

        self.assertEqual(pytest_wrapped_e.type, SystemExit)
        self.assertEqual(str(pytest_wrapped_e.value), f"Unexpected Error on save: {exception_text}\n")

    @patch("management.command.Path")
    @patch("builtins.open")
    def test_save_to_folder_permission_error(self, mock_open, mock_path):
        exception_text = fake.text()
        mock_path.side_effect = PermissionError(exception_text)
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            save_to_folder(self.artist, self.song, self.lyrics)

        self.assertEqual(pytest_wrapped_e.type, SystemExit)
        self.assertEqual(str(pytest_wrapped_e.value), f"Error on save: {exception_text}\n")
    
    @patch("management.command.Path")
    def test_save_to_folder(self, mock_path):
        mock_open = mock.mock_open()
        with mock.patch("builtins.open", mock_open):
            save_to_folder(self.artist, self.song, self.lyrics)
        
        handle = mock_open()
        handle.write.assert_called_once_with(self.lyrics)

