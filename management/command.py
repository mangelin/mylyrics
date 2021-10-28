import argparse
import sys
from slugify import slugify
import os

from pathlib import Path
from management import __version__ as version
from proxy import ProxyLyricsFactory

from config import DEFAULT_SAVE_DIRECTORY


def save_to_folder(artist:str, song_name:str, lyrics:str):
    artist_directory_name = f"{DEFAULT_SAVE_DIRECTORY}/{slugify(artist)}"
    
    try:
        p = Path(artist_directory_name)
        p.mkdir(parents=True)
    except Exception as e:
        print(e)

    file_name = os.path.join(artist_directory_name, f"{slugify(song_name)}.txt")

    with open(file_name,"w+") as f:
        f.write(lyrics)

def load_from_folder(artist:str, song_name:str):
    artist_directory_name = f"{DEFAULT_SAVE_DIRECTORY}/{slugify(artist)}"
    file_name = os.path.join(artist_directory_name, f"{slugify(song_name)}.txt")

    data = None
    try:
        with open(file_name, 'r') as f:
            data = f.read()
    except Exception as e:
        print(e)
    
    return data

class MyLyricsCommand(object):
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-a", "--artist", required=True, help="provide artist name")
        self.parser.add_argument("-l", "--lyrics", required=True, help="provide a lyrics name")
        self.parser.add_argument("-s", "--save",action="store_true",default=False, help="save the song in artist's folder")
        self.parser.add_argument("-p", "--provider", required=True, help="lyrics provider")
        self.parser.add_argument("--version", action="store_true", help="show mylyrics version")

        self.factory = ProxyLyricsFactory()

    def show_version(self):
        sys.stdout.write(f"\nMyLyrics {version}")

    def handle_command(self):
        args = self.parser.parse_args()
        lyrics = None

        if args.version:
            self.show_version()
            sys.exit(0)

        # Try to load from disk
        lyrics = load_from_folder(args.artist, args.lyrics)
        if lyrics:
            sys.stdout.write(lyrics)
            sys.exit(0)

        
        # Try to fetch lyrics by provider
        provider = self.factory.create_proxy(args.provider)
        lyrics = provider.get_lyrics(args.artist, args.lyrics)
    
        if not lyrics:
            sys.stdout.write(f"No lyrics found to {args.lyrics} by {args.artist}")
            sys.exit(0)
        
        sys.stdout.write(lyrics)

        if args.save:
            save_to_folder(args.artist, args.lyrics, lyrics)
