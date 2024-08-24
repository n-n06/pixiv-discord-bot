import pixivpy3
from envconfig import refresh_token
import json
import requests

#authentification and api init
api = pixivpy3.AppPixivAPI()
api.auth(refresh_token=refresh_token)

print(json.dumps(api.illust_detail(119804911), indent=2))


#TODO: implement the partial tag search in the functionality of the bot
#json_result = api.search_illust('水着', search_target='partial_match_for_tags')

#for illust in json_result.illusts:
#    print(illust.title, illust.user.name, illust.id)

#illust = json_result.illusts[0]



#print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))
