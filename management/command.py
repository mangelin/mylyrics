import argparse
import sys
from slugify import slugify
import os

from pathlib import Path
from management import __version__ as version
from proxy import ProxyLyricsFactory
import config


def save_to_folder(artist:str, song_name:str, lyrics:str):
    artist_directory_name = f"{config.DEFAULT_SAVE_DIRECTORY}/{slugify(artist)}"
    
    try:
        p = Path(artist_directory_name)
        p.mkdir(parents=True)

        file_name = os.path.join(artist_directory_name, f"{slugify(song_name)}.txt")

        with open(file_name,"w+") as f:
            f.write(lyrics)
    except PermissionError as ep:
        sys.exit(f"Error on save: {ep}\n")
    except Exception as e:
        sys.exit(f"Unexpected Error on save: {e}\n")

    
def load_from_folder(artist:str, song_name:str):
    artist_directory_name = f"{config.DEFAULT_SAVE_DIRECTORY}/{slugify(artist)}"
    file_name = os.path.join(artist_directory_name, f"{slugify(song_name)}.txt")

    data = None
    try:
        with open(file_name, 'r') as f:
            data = f.read()
    except FileNotFoundError as e:
        pass
    except Exception as e1:
        sys.exit(f"Warning: {e1}\n")
    
    return data

def get_providers(provider_name:str):
    if not provider_name:
        return ProxyLyricsFactory.values()

    r = ProxyLyricsFactory.get(provider_name)
    if not r:
        return None

    return [r]

class MyLyricsCommand(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-a", "--artist", required=True, help="provide artist name")
        self.parser.add_argument("-l", "--lyrics", required=True, help="provide a lyrics name")
        self.parser.add_argument("-s", "--save",action="store_true",default=False, help="save the song in artist's folder")
        self.parser.add_argument("-p", "--provider", help=f"lyrics provider [{','.join(config.providers())}]")
        self.parser.add_argument("--version", action="store_true", help="show mylyrics version")

    def show_version(self):
        sys.stdout.write(f"\nMyLyrics {version}")

    def parse_args(self):
        return self.parser.parse_args() # pragma: no cover

    def handle_command(self):
        args = self.parse_args()
        lyrics = None

        if args.version:
            self.show_version()
            return

        # Try to load from disk
        lyrics = load_from_folder(args.artist, args.lyrics)
        if lyrics:
            sys.stdout.write(lyrics)
            return
        
        # Create provider
        providers = get_providers(args.provider)
        
        if not providers:
            sys.exit(f"error: unknown provider {args.provider}")
        
        # Try to fetch lyrics by provider
        for provider in providers:
        
            try:
                lyrics = provider.get_lyrics(args.artist, args.lyrics)
            except ValueError as e:
                sys.stdout.write(f"{e}\n")
            except Exception as ue:
                sys.stdout.write(f"unexpected error: {ue}\n")

            if lyrics:
                print(lyrics)

                if args.save:
                    save_to_folder(args.artist, args.lyrics, lyrics)

                return

        if not lyrics:
            sys.stdout.write(f"No lyrics found to {args.lyrics} by {args.artist}")
                
        
        