import dotenv
import os

dotenv.load_dotenv("../.env")
token = os.environ.get("TOKEN")
pixiv_username = os.environ.get("PIXIV_USERNAME")
pixiv_password = os.environ.get("PIXIV_PASSWORD")
refresh_token = os.environ.get("REFRESH_TOKEN")
