# This example requires the 'message_content' intent.

import discord
from discord.ext import commands
from pixivpy3 import AppPixivAPI    
import requests
import json
import io
import aiohttp
from bs4 import BeautifulSoup


from config import token, refresh_token 


description = '''
A bot that will (I hope) do cool things with pixiv and other apps

Made by n-n06 on github
'''


intents = discord.Intents.default()
intents.message_content = True
intents.members = True


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
        print('Error connecting to the PixivAPI')


@bot.command()
async def joined(ctx, member: discord.Member):
    '''
    Async Function that sends a message upon a new member joining the server.
    '''
    await ctx.send(f'{member.name} has arrived! {discord.utils.format_dt(member.joined_at)}')


@bot.command(description='Get an illustration from pixiv')
async def illustration(ctx, illust_id: int):
    '''
    Async Function that sends an illustration and an embed to a Discord channel on /illustration.
    The embed contains the illustration url, author name and the illustration name.
    '''

    illustration_url =f'https://www.pixiv.net/en/artworks/{illust_id}'
    
    #this part is necessary for the bot to be able to access pixiv image data 
    headers = {
        'Referer': 'https://www.pixiv.net/'
    }
    
    #send a request to the illust page and parse the response html to get the username, title and the urls
    response = requests.get(illustration_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    illustration_data = soup.find('meta', id='meta-preload-data')['content']
    illustration_data = json.loads(illustration_data)

    username = illustration_data['illust'][str(illust_id)]['userName']
    title = illustration_data['illust'][str(illust_id)]['title']
    image_url = illustration_data['illust'][str(illust_id)]['urls']['regular']

    #start an async session to send the image file to the channel
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url, headers=headers) as resp:
            if resp.status != 200:
                return await ctx.send('Could not download file...')
            data = io.BytesIO(await resp.read())
            
            #TODO: change the embed and the file structure to be sent as one 
            embed = discord.Embed(title=title, url=illustration_url)
            embed.set_author(name=username)
            embed.set_thumbnail(url=image_url)
            await ctx.send(embed=embed, file=discord.File(data, f'{illust_id}.png'))
            #await ctx.send(file=discord.File(data, f'{illust_id}.png'), embed=embed)


bot.run(token)

