import json
from pixivpy3 import AppPixivAPI


from config import refresh_token

app = AppPixivAPI()

app.auth(refresh_token=refresh_token)

result = app.illust_ranking("day")['illusts']
print(*filter(lambda artwork: artwork['type'] == 'illust', result))

s = json.dumps(list(result), indent=2)
print(s)


