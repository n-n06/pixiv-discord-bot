import discord
from discord.ext import commands
from pixivpy3 import AppPixivAPI    
import io
import aiohttp
import typing


from envconfig import token, refresh_token
from botconfig import bot_description, bot_intents, request_headers 
from parsing import PixivParser
from typing_utils import (
    image_size_literal,
    gender_literal,
    r18_literal
)


'''
Instances of bot and api
'''
api = AppPixivAPI()
client = discord.Client(intents=bot_intents)
bot = commands.Bot(command_prefix='/', description=bot_description, intents=bot_intents)

parser = PixivParser(api)


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
    '''Asyncrouniously sends an illustration image to a Discord channel

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
        async with session.get(image_url, headers=request_headers) as resp:
            if resp.status != 200:
                return print('Could not download file...')
            data = io.BytesIO(await resp.read())
            image_file = discord.File(data, f'{illust_id}.png') 
            await ctx.send(title + ' by ' + username + '\n' + tags, file = image_file)
            


@bot.command(description='Get an illustration from pixiv')
async def illustration(ctx, illust_id: int, image_size: image_size_literal = 'medium'):
    '''Sends an illustration and its info to a Discord channel on /illustration.
    
    Sends an illustration's image of a particular size to a Discord channel.
    Then, sends general information about the illustration.

    NOTE: the image will not be displayed without the headers in the request

    Args:
        illust_id: int. An identifier of the illustration on Pixiv
        image_size: str. By default, set to 'medium'.

    Raises:
        Illusration not Found if the page for the illustration
          is missing

        Illusration Set to Invinsible if the illust is set to Invinsible
          by either the user or the author
        
    '''

    illust_detail = api.illust_detail(illust_id)

    
    try:
        username, title, image_url, tags = parser.parse_illust(illust_detail, image_size)
    except Exception as e:
        await ctx.send(e)
        return
        

    await send_illustration(ctx, illust_id, username, title, tags, image_url)
             


@bot.command(description='Get daily rankings from pixiv')
async def daily(ctx, 
                gender: gender_literal,
                r18: r18_literal,
                limit : typing.Optional[int], 
                image_size: image_size_literal = 'medium'): 
    '''Sends daily rankings from pixiv to a Discord channel on /daily
        
    Sends a limited number of illustrations that are trending today 
      among the users of pixiv. Supports ranking specifications 
      such as gender, supports filtering R18 arts.

    Args:
        limit: int. Optional. Number of illustrations to send
        image_size: str. By default, set to 'medium'
        gender: str. Optional. Either male or female
          Specifies ranking's gender criteria
        r18: str. Optional. Can be either omited or specified as r18

    Returns:
        None
    
    Raises:
        Illusration not Found if the page for the illustration
          is missing

        Illusration Set to Invinsible if the illust is set to Invinsible
          by either the user or the author   
    '''

    daily_illusts_details = parser.parse_daily_rankings(gender, r18, limit)


    for illust in daily_illusts_details:
        try:
            illust_id, username, title, image_url, tags = parser.parse_illust_detail(illust, image_size)
        except Exception as e:
            await ctx.send(e)
            return

        await send_illustration(ctx, illust_id, username, title, tags, image_url)



@bot.command(description = 'Get weekly rankings from pixiv')
async def weekly(ctx,
                 limit: typing.Optional[int],
                 details: typing.Optional[typing.Literal['rookie', 'r18']],
                 image_size: typing.Literal['medium', 'large', 'original'] = 'medium'):
    '''Sends weekly rankings from pixiv to a Discord channel on /weekly
    
    Sends a limited number of illustrations that are trending this week 
      among the users of pixiv. Supports ranking specifications 
      such as artist experience and filtering R18 arts.

    Args:
        limit: int. Optional. Number of illustrations to send
        details: str. Optinal. Weekly ranking specification.
          Either rookie (arts by amateur artists) or r18
        image_size: str. By default, set to 'medium'

    Returns:
        None
    
    Raises:
        Illusration not Found if the page for the illustration
          is missing

        Illusration Set to Invinsible if the illust is set to Invinsible
          by either the user or the author   
    '''
    mode = 'week'

    if details:
        mode = mode + '_' + details

    
    #filtering out non-illust artworks
    weekly_illusts_details = list(filter(lambda artwork: artwork['type'] == 'illust', api.illust_ranking(mode)['illusts']))
        
    if limit:
        weekly_illusts_details = weekly_illusts_details[:limit]


    for illust in weekly_illusts_details:
        try:
            illust_id, username, title, image_url, tags = parser.parse_illust_detail(illust, image_size)
        except Exception as e:
            await ctx.send(e)
            return

        await send_illustration(ctx, illust_id, username, title, tags, image_url)
   


@bot.command(description = 'Get monthly rankings from pixiv')
async def monthly(ctx, limit: typing.Optional[int], image_size: typing.Literal['medium', 'large', 'original'] = 'medium'):
    '''Sends monthly rankings from pixiv to a Discord channel on /monthly
    
    Sends a limited number of top illustrations this month
      Does not support specifications

    Args:
        limit: int. Optional. Number of illustrations to send
        image_size: str. By default, set to 'medium'

    Returns:
        None
    
    Raises:
        Illusration not Found if the page for the illustration
          is missing

        Illusration Set to Invinsible if the illust is set to Invinsible
          by either the user or the author   
    '''

    
    montly_illusts_details = list(filter(lambda artwork: artwork['type'] == 'illust', api.illust_ranking('month')['illusts'])) 

    if limit:
        montly_illusts_details = montly_illusts_details[:limit]

    for illust in montly_illusts_details:
        try:
            illust_id, username, title, image_url, tags = parser.parse_illust_detail(illust, image_size)
        except Exception as e:
            await ctx.send(e)
            return

        await send_illustration(ctx, illust_id, username, title, tags, image_url)



bot.run(token)
'''
TODO:
1. weekly / monthly rankings illust_ranking
    -basic functionality done
    -divide into class method of Parser
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





