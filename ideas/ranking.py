import json
from pixivpy3 import AppPixivAPI

from config import refresh_token

app = AppPixivAPI()

app.auth(refresh_token=refresh_token)

result = app.illust_ranking("day")
result = json.dumps(result, indent=2)

result = json.loads(result)
result = result['illusts']
print(len(result))
illust_only = list(filter(lambda artwork: artwork['type'] == 'illust', result))
print(len(illust_only))

print("\n")
s = json.dumps(illust_only, indent=2)
print(s)


#
# s = json.dumps(list(result), indent=2)
# print(s)





