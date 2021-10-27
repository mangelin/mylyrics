from dotenv import load_dotenv
import os

load_dotenv()

AZLYRICS_PROXY="AZLyrics"
ELYRICS_PROXY="ELyrics"

AZLYRICS_SEARCH_URL = os.getenv("AZLYRICS_SEARCH_URL")

ELYRICS_BASE_URL = os.getenv("ELYRICS_BASE_URL")
ELYRICS_SEARCH_URL = f"{ELYRICS_BASE_URL}/find.php"

OUTPUT_FORMAT = os.getenv("DEFAULT_OUTPUT_FORMAT")

DEFAULT_SAVE_DIRECTORY = os.getenv("DEFAULT_SAVE_DIRECTORY", os.curdir)