from pixivpy_async import AppPixivAPI
from parsing import pixiv_parser

api = AppPixivAPI()

parser = pixiv_parser.PixivParser(api)
