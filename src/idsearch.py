from os import walk
from pixivpy3 import AppPixivAPI
import requests
from config import refresh_token
from parsing import parse_illust_detail

app = AppPixivAPI()
app.auth(refresh_token=refresh_token)


result2 = app.illust_detail(110221098)

#print(json_result['illust']['image_urls']['medium'])
#print(json_result['illust']['caption'])
#print(json_result['illust']['user']['name'])

headers = {
    'Referer': 'https://www.pixiv.net/'
}


values = parse_illust_detail(result2, 'medium')
print(values)


