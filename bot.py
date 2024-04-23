# This example requires the 'message_content' intent.

import discord
import os
import pufferpanel_api
from dotenv import load_dotenv
from typing import Literal

load_dotenv()
token = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


@tree.command(
    name='start',
    description='Starts a server',
    guild=discord.Object(id=966113895288819722))
@discord.app_commands.describe(server='The server to start')
async def startServer(interaction: discord.Interaction, server: Literal[tuple(pufferpanel_api.get_servers())]):
    await interaction.response.send_message('Starting ' + server + '!')
    pufferpanel_api.start_server(pufferpanel_api.get_servers()[server])


@tree.command(
    name='stop',
    description='Stops a server',
    guild=discord.Object(id=966113895288819722))
@discord.app_commands.describe(server='The server to stop')
async def stopServer(interaction: discord.Interaction, server: Literal[tuple(pufferpanel_api.get_servers())]):
    await interaction.response.send_message('Stopping ' + server + '!')
    pufferpanel_api.stop_server(pufferpanel_api.get_servers()[server])


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=966113895288819722))
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


client.run(token)
