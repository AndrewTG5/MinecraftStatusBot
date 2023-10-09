import os
import discord
import socket
import asyncio
import time
import urllib.request
import datetime
from mcstatus import MinecraftServer
from discord.ext import tasks, commands

now = datetime.datetime.now()

TOKEN = ''
GUILD = ''
CHANNEL = 
bot = commands.Bot(command_prefix='!')
IPAddress = 1
IPAddress0 = 0


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        '[' + now.strftime("%Y-%m-%d %H:%M:%S") + ']    '+ 'bot started'
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


@tasks.loop(minutes=1)
async def IP_Address_Check():
    global IPAddress0
    global IPAddress
    IPAddress = urllib.request.urlopen(
        'https://ident.me').read().decode('utf8')
    if IPAddress != IPAddress0:
        IPAddress0 = urllib.request.urlopen(
            'https://ident.me').read().decode('utf8')
        print('[' + now.strftime("%Y-%m-%d %H:%M:%S") + ']    ' +
              'sending new address: ' + IPAddress0)
        await bot.get_channel(CHANNEL).send(f'New Server IP Address \n  \n {IPAddress0}:7777')
    else:
        print('[' + now.strftime("%Y-%m-%d %H:%M:%S") + ']    ' +
              'checked IP, no change')
    Players = MinecraftServer.lookup(
        str(IPAddress)+':7777').status().players.online
    print('[' + now.strftime("%Y-%m-%d %H:%M:%S") + ']    ' +
          'setting presence to ' + str(Players) + ' players')
    if Players == 1:
        await bot.change_presence(activity=discord.Game('with ' + str(Players) + ' other player'))
    else:
        await bot.change_presence(activity=discord.Game('with ' + str(Players) + ' other players'))


async def manualCheck():
    global IPAddress0
    global IPAddress
    IPAddress = urllib.request.urlopen(
        'https://ident.me').read().decode('utf8')
    if IPAddress != IPAddress0:
        IPAddress0 = urllib.request.urlopen(
            'https://ident.me').read().decode('utf8')
        print('[' + now.strftime("%Y-%m-%d %H:%M:%S") + ']    ' +
              'sending new address: ' + IPAddress0)
        await bot.get_channel(CHANNEL).send(f'New Server IP Address \n  \n {IPAddress0}:7777')
    else:
        print('[' + now.strftime("%Y-%m-%d %H:%M:%S") + ']    ' +
              'checked IP, no change')
    Players = MinecraftServer.lookup(
        str(IPAddress)+':7777').status().players.online
    print('[' + now.strftime("%Y-%m-%d %H:%M:%S") + ']    ' +
          'setting presence to ' + str(Players) + ' players')
    if Players == 1:
        await bot.change_presence(activity=discord.Game('with ' + str(Players) + ' other player'))
    else:
        await bot.change_presence(activity=discord.Game('with ' + str(Players) + ' other players'))


@IP_Address_Check.before_loop
async def wait_for_bot():
    await bot.wait_until_ready()
    global IPAddress
    global IPAddress0
    IPAddress = urllib.request.urlopen(
        'https://ident.me').read().decode('utf8')
    IPAddress0 = urllib.request.urlopen(
        'https://ident.me').read().decode('utf8')
    print('[' + now.strftime("%Y-%m-%d %H:%M:%S") + ']    ' +
          'sending new address: ' + IPAddress0)
    await bot.get_channel(CHANNEL).send(f'New Server IP Address \n  \n {IPAddress0}:7777')


@bot.command()
async def players(ctx):
    print('[' + now.strftime("%Y-%m-%d %H:%M:%S") + ']    ' +
          'sending current players list')
    query = MinecraftServer.lookup(str(IPAddress)+':7777').query()
    await ctx.send(
        "players: {}/{} {}".format(
            query.players.online,
            query.players.max,
            query.players.names,
        )
    )

@bot.command()
async def stats(ctx):
    print('[' + now.strftime("%Y-%m-%d %H:%M:%S") + ']    ' +
          'sending server query stats')
    query = MinecraftServer.lookup(str(IPAddress)+':7777').query()
    await ctx.send(
        "host: {}:{}".format(query.raw['hostip'], query.raw['hostport']) + '\n' +
        "software: v{} {}".format(query.software.version, query.software.brand) + '\n' +
        "plugins: {}".format(query.software.plugins) + '\n' +
        "motd: \"{}\"".format(query.motd) + '\n' +
        "players: {}/{} {}".format(
            query.players.online,
            query.players.max,
            query.players.names,
        )
    )


@bot.command()
async def refresh(ctx):
    print('[' + now.strftime("%Y-%m-%d %H:%M:%S") + ']    ' +
          'manual refresh triggered')
    manualCheck()
    await ctx.send('refreshed')


@bot.command()
async def h(ctx):
    print('[' + now.strftime("%Y-%m-%d %H:%M:%S") + ']    ' + 'sending bot help')
    await ctx.send(
        '!h: brings up this help message \n'
        '!refresh: tells bot to refresh IP and player numbers \n'
        '!stats: gives detailed info about the server, including names of who is ingame \n'
        '!players: gives the names of players currently ingame'
    )


IP_Address_Check.start()
bot.run(TOKEN)
