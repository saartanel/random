"""
Discord Chuck Norris joke bot
"""

import discord
import requests

token = "" #Discord bot token

client = discord.Client()


def chuckJoke():
    """
    Get a random Chuck Norris joke.
    """
    data = requests.get('https://api.chucknorris.io/jokes/random')
    joke = data.json()["value"]
    return joke


@client.event
async def on_ready():
    """
    Login to Discord
    """
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    """
    Send message
    :param message:
    :return:
    """
    username = str(message.author).split('#')[0]
    userMessage = str(message.content)
    channel = str(message.channel.name)
    print(f'{username}: {userMessage} ({channel})')

    if message.author == client.user:
        return

    if userMessage.lower() == '!chuck':
        await message.channel.send(chuckJoke())
        return


client.run(token)
