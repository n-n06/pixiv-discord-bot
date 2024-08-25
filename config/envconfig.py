'''A module to load private information from .env file

Loads tokens and passwords from the .env file that can
  be used in other modules or scripts.
'''

import dotenv
import os

dotenv.load_dotenv()
token = os.environ.get("TOKEN")
#pixiv_username = os.environ.get("PIXIV_USERNAME")
#pixiv_password = os.environ.get("PIXIV_PASSWORD")
refresh_token = os.environ.get("REFRESH_TOKEN")

