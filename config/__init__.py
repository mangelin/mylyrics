from dotenv import load_dotenv
import os

load_dotenv()

AZLYRICS_SEARCH_URL = os.getenv("AZLYRICS_SEARCH_URL")
ELYRICS_SEARCH_URL = os.getenv("ELYRICS_SEARCH_URL")