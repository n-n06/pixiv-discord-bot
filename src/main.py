import discord
from discord.ext import commands
from pixivpy3 import AppPixivAPI    
import io
import aiohttp


from config import token, refresh_token 
from parsing import display_tags, parse_illust_detail


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




@bot.command(description='Get an illustration from pixiv')
async def illustration(ctx, illust_id: int, image_size: str = 'medium'):
    '''
    Sends an illustration to a Discord channel on /illustration.
    
    Sends an illustration's image of a particular size to a Discord channel.
    Then, sends general information about the illustration.

    NOTE: the image will not be displayed without the headers in the request

    Args:
        illust_id: int. An identifier of the illustration on Pixiv
        image_size: str. By default, set to 'medium'

    '''

    
    #this part is necessary for the bot to be able to access pixiv image data 
    headers = {
        'Referer': 'https://www.pixiv.net/'
    }

    try:
        illust_detail = api.illust_detail(illust_id)
    except:
        raise(ValueError('Invalid illust_id'))


    
    try:
        username, title, image_url, tags = await parse_illust_detail(illust_detail, image_size)
    except Exception as e:
        await ctx.send(e)
        return
        

    #start an async session to send the image file to the channel
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url, headers=headers) as resp:
            if resp.status != 200:
                return await ctx.send('Could not download file...')
            data = io.BytesIO(await resp.read())
            await ctx.send(file = discord.File(data, f'{illust_id}.png'))
            await ctx.send(title + ' by ' + username)
            await display_tags(ctx, tags)
             


bot.run(token)

