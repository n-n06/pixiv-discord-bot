import discord
from discord.ext import commands
from pixivpy3 import AppPixivAPI    
import io
import aiohttp
import typing

from config import token, refresh_token 
from parsing import parse_illust_detail


'''
Basic Bot Configuration
'''
description = '''
A bot that will (I hope) do cool things with pixiv and other apps

Made by n-n06 on github
'''

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

headers = {
    'Referer': 'https://www.pixiv.net/'
}

'''
Instances of bot and api
'''
api = AppPixivAPI()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='/', description=description, intents=intents)





@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    try:
        api.auth(refresh_token=refresh_token)
        print('Logged into PixivAPI')
        print('------')
    except:
        raise(ConnectionError('Error connecting to the PixivAPI'))


async def send_illustration(ctx, illust_id : int, username : str, title : str, tags : str, image_url : str):
    '''Asyncrouniously sends an illustration to a Discord channel

    Args:
        illust_id: int. An identifier of the illustration.
          Used to name the image file
        username: str. The illustration's creator
        title: str
        tags: str
        image_url: str. A URL to the image on pximg.net

    Returns:
        None

    '''
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url, headers=headers) as resp:
            if resp.status != 200:
                return print('Could not download file...')
            data = io.BytesIO(await resp.read())
            await ctx.send(title + ' by ' + username + '\n' + tags, file = discord.File(data, f'{illust_id}.png'))
            #await ctx.send(title + ' by ' + username + '\n' + display_tags(tags))


@bot.command(description='Get an illustration from pixiv')
async def illustration(ctx, illust_id: int, image_size: str = 'medium'):
    '''Sends an illustration to a Discord channel on /illustration.
    
    Sends an illustration's image of a particular size to a Discord channel.
    Then, sends general information about the illustration.

    NOTE: the image will not be displayed without the headers in the request

    Args:
        illust_id: int. An identifier of the illustration on Pixiv
        image_size: str. By default, set to 'medium'

    Raises:
        Illusration not Found: if the page for the illustration
          is missing

        Illusration Set to Invinsible: if the illust is set to Invinsible
          by either the user or the author
        
    '''

    illust_detail = api.illust_detail(illust_id)

    
    try:
        username, title, image_url, tags = parse_illust_detail(illust_detail, image_size)
    except Exception as e:
        await ctx.send(e)
        return
        

    #start an async session to send the image file to the channel
    await send_illustration(ctx, illust_id, username, title, tags, image_url)

    #recommendation_text = f'You can use /recommend {illust_id} to get recommended artworks'
    #await ctx.send(recommendation_text)
             

@bot.command(description='Get daily rankings from pixiv')
async def daily(ctx, 
                limit : typing.Optional[int], 
                gender: typing.Optional[typing.Literal['male', 'female']],
                r18: typing.Optional[typing.Literal['nsfw']],
                image_size: str = 'medium'): 
    '''Sends daily rankings from pixiv to a Discord channel on /daily

    Args:
        limit: Optional[int] - the number of illustrations to send
        image_size: str
        gender: str. Either male or female (in this case. not in general)
          Specifies ranking's gender criteria
        r18: str. Optional. Can be either omited or specified as NSFW

    Returns:
        None
    
    Raises:
        Illusration not Found: if the page for the illustration
          is missing

        Illusration Set to Invinsible: if the illust is set to Invinsible
          by either the user or the author   
    '''
    mode = 'day'
    if gender:
        mode = mode + '_' + gender
    if r18:
        mode = mode + '_' + 'r18'

    print(mode)
    
    #filtering out non-illust artworks
    daily_illusts_details = list(filter(lambda artwork: artwork['type'] == 'illust',api.illust_ranking(mode)['illusts']))
        
    if limit:
        daily_illusts_details = daily_illusts_details[:limit]


    for illust in daily_illusts_details:
        try:
            illust_id, username, title, image_url, tags = parse_illust_detail(illust, image_size)
        except Exception as e:
            await ctx.send(e)
            return

        await send_illustration(ctx, illust_id, username, title, tags, image_url)


@bot.command(description = 'Get weekly rankings from pixiv')
async def weekly(ctx, limit: typing.Optional[int], image_size: str = 'medium'):
    pass
    

@bot.command(description = 'Get monthly rankings from pixiv')
async def monthly(ctx, limit: typing.Optional[int], image_size: str = 'medium'):
    pass




bot.run(token)
'''
TODO:
1. weekly / monthly rankings illust_ranking
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
