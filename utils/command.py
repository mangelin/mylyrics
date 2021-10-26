import argparse

from utils import __version__ as version
from proxy import ProxyLyricsFactory

class MyLyricsCommand(object):
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-a", "--artist", help="provide artist name")
        self.parser.add_argument("-l", "--lyrics", help="provide a lyrics name")
        self.parser.add_argument("-s", "--save",action="store_true",default=False, help="save the song in artist's folder")
        self.parser.add_argument("-p", "--provider", help="lyrics provider")
        self.parser.add_argument("--version", action="store_true", help="show mylyrics version")

        self.factory = ProxyLyricsFactory()

    def show_version(self):
        print(f"\nMyLyrics {version}")

    def handle_command(self):
        args = self.parser.parse_args()

        if args.version:
            self.show_version()

        if args.artist and args.lyrics:
            print(f'Artist: {args.artist}')
            print(f'Lyrics: {args.lyrics}')

        if args.provider:
            provider = self.factory.create_proxy(args.provider)
            song = provider.get_song(args.artist, args.lyrics)
            print(song)
