# This example requires the 'message_content' intent.

import discord
from discord.ext import commands
from pixivpy3 import AppPixivAPI    
import requests

from config import token, refresh_token 


description = '''
A bot that will (I hope) do cool things with pixiv and other apps

Made by n-n06 on github
'''


intents = discord.Intents.default()
intents.message_content = True
intents.members = True


api = AppPixivAPI()
api.auth(refresh_token=refresh_token)
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="/", description=description, intents=intents)



@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def joined(ctx, member: discord.Member):
    await ctx.send(f"{member.name} has arrived! {discord.utils.format_dt(member.joined_at)}")

@bot.command(description="Get an illust from pixiv")
async def illustration(ctx, illust_id: int, image_size: str):
    image_size = image_size.lower() 

    illustration = api.illust_detail(illust_id).illust
    illustration_url =f"https://www.pixiv.net/en/artworks/{illustration['id']}"
    image_url = illustration["image_urls"][image_size]

    # Create an embed for Discord 

    embed = discord.Embed(title=illustration['title'], url=illustration_url)
    embed.set_image(url=image_url)
    embed.set_author(name=f'{illustration["user"]["name"]}')


    # Send the embed as a message in the channel
    await ctx.send(embed=embed)



bot.run(token)

