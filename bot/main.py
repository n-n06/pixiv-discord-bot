from config import bot, api 
from config import token, refresh_token 
from bot_commands import *
from utils.typing_utils import *


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    try:
        await api.login(refresh_token=refresh_token)
        print('Logged into PixivAPI')
        print('------')
    except:
        raise(ConnectionError('Error connecting to the PixivAPI'))


bot.run(token)


'''
TODO:
1. weekly / monthly rankings illust_ranking
    -basic functionality done
    -divide into class method of Parser done
    -
2. tag search search_illust with limit
3. illust_related, illust_recommended with limit
4. user_detail, user_illusts with limit





Final functionality:
1. illust by id
2. daily / weekly / monthly rankings (same function but different args)
3. tag search 
4. get related illusts
5. get illustrations of a user or info about the user





'''





