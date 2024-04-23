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

servers = pufferpanel_api.get_servers()


@tree.command(
    name='start',
    description='Starts a server')
@discord.app_commands.describe(server='The server to start')
async def startServer(interaction: discord.Interaction, server: Literal[tuple(servers)]):
    await interaction.response.send_message('Starting ' + server + '!')
    pufferpanel_api.start_server(servers[server])


@tree.command(
    name='stop',
    description='Stops a server')
@discord.app_commands.describe(server='The server to stop')
async def stopServer(interaction: discord.Interaction, server: Literal[tuple(servers)]):
    await interaction.response.send_message('Stopping ' + server + '!')
    pufferpanel_api.stop_server(servers[server])


@tree.command(
    name='servers',
    description='Lists all servers')
async def listServers(interaction: discord.Interaction):
    global servers
    servers = pufferpanel_api.get_servers()
    serverstring = ""
    for server in servers:
        if pufferpanel_api.get_server_status(servers[server]):
            serverstring += ':white_check_mark: ' + server + '\n'
        else:
            serverstring += ':octagonal_sign: ' + server + '\n'

    await interaction.response.send_message(serverstring)


@client.event
async def on_ready():
    await tree.sync()
    print(f'We have logged in as {client.user}')


client.run(token)
