from io import StringIO
from random import randrange
from typing import Iterator
from unittest import TestCase, mock
from unittest.mock import MagicMock, Mock, create_autospec, patch

from faker import generator

import config
import pytest
from management import MyLyricsCommand
from management import __version__ as version
from management.command import get_providers, get_providers, load_from_folder, save_to_folder
from proxy import ProxyLyricsFactory
import types

from tests import fake

from .factory import CommandParserFactory

providers = config.providers()

class MyLyricsCommandTestCase(TestCase):
    def setUp(self) -> None:
        self.cmd = MyLyricsCommand()
        self.args = Mock()

        self.lyrics = fake.text()
        self.artist = fake.name()
        self.song = fake.name()
        self.provider = providers[randrange(0,len(providers))]

        self.fake_proxy = Mock()
        self.fake_proxy.name = fake.name()
        self.fake_proxy.get_lyrics.return_value = self.lyrics

        self.factory = Mock()
        self.factory.get.return_value = self.fake_proxy
        self.factory.values.return_value = [self.fake_proxy,self.fake_proxy]

        self.factory_no_provider = Mock()
        self.factory_no_provider.get.return_value = None
        


    
    def test_get_version(self):
        with patch('sys.stdout', new = StringIO()) as fake_out:
            self.cmd.show_version()
            self.assertEqual(fake_out.getvalue(), f"\nMyLyrics {version}")

    def test_handle_command_show_version(self):
        with patch('management.command.MyLyricsCommand.parse_args') as mock_parse_args:
            mock_args = CommandParserFactory.create_args(version=True)
            mock_parse_args.return_value = mock_args
            with patch('sys.stdout', new = StringIO()) as fake_out:
                self.cmd.handle_command()
                self.assertEqual(fake_out.getvalue(), f"\nMyLyrics {version}")

    
    @patch("management.command.load_from_folder")
    def test_handle_command_load_from_folder(self, mock_load):
        mock_load.return_value = self.lyrics

        with patch('management.command.MyLyricsCommand.parse_args') as mock_parse_args:
            mock_args = CommandParserFactory.create_args(
                version=False, 
                artist=self.artist,
                lyrics = self.song,
                provider = self.provider
            )
            mock_parse_args.return_value = mock_args
            with patch('sys.stdout', new = StringIO()) as fake_out:
                self.cmd.handle_command()
                self.assertEqual(fake_out.getvalue(), self.lyrics)

    @patch("requests.get")
    @patch("requests.post")
    @patch("management.command.load_from_folder")
    def test_handle_command_requests_error(self,mock_load, mock_post, mock_get):
        mock_post.side_effect = Exception
        mock_get.side_effect = Exception
        mock_load.return_value = None

        with patch('management.command.MyLyricsCommand.parse_args') as mock_parse_args:
            mock_args = CommandParserFactory.create_args(
                version=False, 
                artist=self.artist,
                lyrics = self.song,
                provider = self.provider
            )
            mock_parse_args.return_value = mock_args
            with patch('sys.stdout', new = StringIO()) as fake_out:
                self.cmd.handle_command()
                self.assertIn("unexpected error:",fake_out.getvalue())

    

    @patch("management.command.get_providers")
    @patch("management.command.load_from_folder")
    def test_handle_command_lyrics_error(self,mock_load, mock_p):
        
        mock_load.return_value = False
        mock_p.return_value = [self.fake_proxy]

        error_text = fake.text()
        self.fake_proxy.get_lyrics.side_effect = ValueError(error_text)

        
        with patch('management.command.MyLyricsCommand.parse_args') as mock_parse_args:
            mock_args = CommandParserFactory.create_args(
                version=False, 
                artist=self.artist,
                lyrics = self.song,
                provider = self.provider,   
                save = False
            )
            
            mock_parse_args.return_value = mock_args

            with patch('sys.stdout', new = StringIO()) as fake_out:
                self.cmd.handle_command()
                self.assertIn(error_text, fake_out.getvalue())
                self.assertIn(f"No lyrics found to {self.song} by {self.artist}", fake_out.getvalue())
                
            self.fake_proxy.get_lyrics.side_effect = None
            self.fake_proxy.get_lyrics.return_value = None
            with patch('sys.stdout', new = StringIO()) as fake_out:
                self.cmd.handle_command()
                self.assertIn("No lyrics found to", fake_out.getvalue())




    @patch("management.command.get_providers")
    @patch("management.command.load_from_folder")
    def test_handle_command_all_ok_no_save(self,mock_load, mock_p):
        
        mock_load.return_value = False
        mock_p.return_value = [self.fake_proxy]
        
        with patch('management.command.MyLyricsCommand.parse_args') as mock_parse_args:
            mock_args = CommandParserFactory.create_args(
                version=False, 
                artist=self.artist,
                lyrics=self.song,
                provider=self.provider,   
                save=False
            )
            mock_parse_args.return_value = mock_args

            with patch('sys.stdout', new = StringIO()) as fake_out:
                self.cmd.handle_command()
                self.assertEqual(fake_out.getvalue(), self.lyrics+"\n")

    @patch("management.command.get_providers")
    @patch("management.command.Path")
    @patch("management.command.load_from_folder")
    def test_handle_command_all_ok_and_save(self,mock_load, mock_path, mock_p):
        
        mock_load.return_value = False
        mock_p.return_value = [self.fake_proxy]
        
        with patch('management.command.MyLyricsCommand.parse_args') as mock_parse_args:
            mock_args = CommandParserFactory.create_args(
                version=False, 
                artist=self.artist,
                lyrics =self.song,
                provider=self.provider,   
                save=True
            )
            
            mock_parse_args.return_value = mock_args

            mock_open = mock.mock_open()
            with mock.patch("builtins.open", mock_open):
                self.cmd.handle_command()
                
                handle = mock_open()
                handle.write.assert_called_once_with(self.lyrics)

    @patch("management.command.Path")
    @patch("management.command.load_from_folder")
    @patch("management.command.get_providers")
    def test_handle_command_no_providers_found(self, mock_getp, mock_load, mock_path):
        mock_load.return_value = False
        mock_getp.return_value = []
        fake_provider = fake.name()

        expected_message = f"No lyrics found to {self.song} by {self.artist} with providers :"
        
        with patch('management.command.MyLyricsCommand.parse_args') as mock_parse_args:
            mock_args = CommandParserFactory.create_args(
                version=False, 
                artist=self.artist,
                lyrics =self.song, 
                save=True,
                provider=fake_provider
            )
            
            mock_parse_args.return_value = mock_args

            with patch('sys.stdout', new = StringIO()) as fake_out:
                self.cmd.handle_command()
                self.assertIn(expected_message, fake_out.getvalue())

            
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


    def test_get_providers(self):
        fp1 = fake.name()
        
        res = get_providers(None)
        self.assertTrue(isinstance(res,types.GeneratorType))
        for r in res:
            self.assertTrue(r in list(ProxyLyricsFactory.values()))

        res = get_providers(fake.name())
        self.assertTrue(isinstance(res,types.GeneratorType))
        self.assertTrue(len(list(res))==0)            

