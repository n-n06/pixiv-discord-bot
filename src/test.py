from os import walk
from pixivpy3 import AppPixivAPI
import requests
from config import refresh_token

app = AppPixivAPI()
app.auth(refresh_token=refresh_token)

json_result = app.illust_detail(1618456)

#print(json_result['illust']['image_urls']['medium'])
#print(json_result['illust']['caption'])
#print(json_result['illust']['user']['name'])

headers = {
    'Referer': 'https://www.pixiv.net/'
}

print(json_result['illust']['tags'])
print(json_result['illust']['meta_single_page'])

response = requests.get(json_result['illust']['image_urls']['medium'], headers=headers)


