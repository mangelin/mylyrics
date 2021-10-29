from dotenv import load_dotenv
import os

load_dotenv()
__PROVIDERS = []

def register_provider(provider_name):
    __PROVIDERS.append(provider_name)

def providers():
    return list(map(lambda p:p.lower(),__PROVIDERS))

# DEAFULT PROVIDERS
#############################################################
AZLYRICS_PROXY="AZLyrics"
ELYRICS_PROXY="ELyrics"

register_provider(AZLYRICS_PROXY)
register_provider(ELYRICS_PROXY)

# ENVS
#############################################################
AZLYRICS_SEARCH_URL = os.getenv("AZLYRICS_SEARCH_URL")
ELYRICS_BASE_URL = os.getenv("ELYRICS_BASE_URL")
ELYRICS_SEARCH_URL = f"{ELYRICS_BASE_URL}/find.php"
OUTPUT_FORMAT = os.getenv("DEFAULT_OUTPUT_FORMAT")
DEFAULT_SAVE_DIRECTORY = os.getenv("DEFAULT_SAVE_DIRECTORY", os.curdir)

# USER CONFIG
#############################################################