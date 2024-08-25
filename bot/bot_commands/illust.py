import aiohttp
import io
import discord

from config import request_headers
from config import bot, parser
from utils.typing_utils import *
from utils.exceptions import IllustrationInvinsible, IllustrationNotFound

async def send_illustration(ctx, illust_id : int, username : str, title : str, tags : str, image_url : str):
    '''Asyncrouniously sends an illustration image to a Discord channel
    
    NOTE: The request headers in the aiohttp session are 
      essential for proper functionality. Do NOT remove them

    Args:
        illust_id: int. An identifier of the illustration.
          Used to name the image file
        username: str. The author's username
        title: str
        tags: str. Comma separated tags
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
    
    Sends an illustration's image to a Discord channel.
    Then, sends general information about the illustration.


    Args:
        illust_id: int. An identifier of the illustration on Pixiv
        image_size: Literal['medium', 'large', 'original'].
          By default, set to 'medium'.

    Returns:
        None

    Raises (sends Exception message to the channel):
        Illusration not Found if the page for the illustration
          is missing

        Illusration Set to Invinsible if the illust is set to Invinsible
          by either the user or the author   
        
    '''
    
    try:
        username, title, tags, image_url = await parser.parse_illust(illust_id, image_size)
    except (IllustrationInvinsible, IllustrationNotFound) as e:
        await ctx.send(e)
        return
        

    await send_illustration(ctx, illust_id, username, title, tags, image_url)
