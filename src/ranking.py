import json
from pixivpy3 import AppPixivAPI


from config import refresh_token

app = AppPixivAPI()

app.auth(refresh_token=refresh_token)

result = app.illust_ranking("day")

#s = json.dumps(result, indent=2)
#print(s)

for illust in result['illusts']:
    print(illust['title'], illust['user']['name'])
