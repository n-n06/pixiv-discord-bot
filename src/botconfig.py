import discord

'''
Basic Bot Configuration
'''

bot_description = '''
A bot that will (I hope) do cool things with pixiv and other apps

Made by n-n06 on github
'''

bot_intents = discord.Intents.default()
bot_intents.message_content = True
bot_intents.members = True

request_headers = {
    'Referer': 'https://www.pixiv.net/'
}
