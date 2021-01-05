import asyncio
import json
import os
import time
from datetime import date
import copy
import wikipedia

import discord
import discord.ext.commands as commands
from discord.utils import get

from constants import *
from cogs.verification import VerificationCog
from cogs.help import HelpCog
from cogs.songs import SongsCog
from cogs.calendar import CalendarCog

from collections import Counter
from difflib import SequenceMatcher

prefix = "-"
client = commands.Bot(command_prefix=prefix, description='A simple RPG bot')
client.remove_command("help")

class local:
    SERVER_DATA = {}
    CALENDAR_DATA = {}
    last_india = time.time()
    
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

async def save_data():
    '''
    - Periodically saves PLAYER_DATA as a json file
    '''

    while True:
        minutes = 5
        await asyncio.sleep(60*minutes)

        with open('server_data.json', 'w') as f:
            json.dump(local.SERVER_DATA, f, indent=4)
            print('[=] Server-data json successfully updated')
        
        with open('calendar_data.json', 'w') as f:
            json.dump(local.CALENDAR_DATA, f, indent=4)
            print('[=] Calendar-data json successfully updated')

async def change_status():

    while True:
        minutes = 0.1
        await asyncio.sleep(60*minutes)
        velo = client.get_guild(id=439916795554430986)
        bots = ['VelociraptorBot','TacoShack','Octave','Rythm']
        counter = [m for m in velo.members if m.status in [discord.Status.online, discord.Status.do_not_disturb] and m.name not in bots]

        games = []
        talkers = 0
        for i in counter:
            try:
                g = i.activity.name
                if g.lower() != g and g != None:
                    games.append(g)
            except:
                talkers += 1


        if len(games) > 0:
            mode = max(set(games), key=games.count)
            activity = discord.Game(name=mode)
        else:
            mode = None
            activity = discord.Game(name=f"")
        
        await client.change_presence(status=discord.Status.online, activity=activity)

client.loop.create_task(save_data())
client.loop.create_task(change_status())

@client.event
async def on_ready():

    print(f'We have logged in as {client.user}')
    print("------------")

    if os.path.exists("server_data.json"):
        with open('server_data.json', 'r') as f:

            local.SERVER_DATA = json.load(f)
            # Merges player data with 'default data' to account for new keys
            print("[=] Server-data file properly loaded")
    else:
        with open('server_data.json', 'w') as f:
            json.dump({}, f)
            print('[+] New Server-data file')

    if os.path.exists("calendar_data.json"):
        with open('calendar_data.json', 'r') as f:

            local.CALENDAR_DATA = json.load(f)
            # Merges player data with 'default data' to account for new keys
            print("[=] Calendar-data file properly loaded")
    else:
        with open('calendar_data.json', 'w') as f:
            calendar = {
                "Monday" : [],
                "Tuesday" : [],
                "Wednesday" : [],
                "Thursday" : [],
                "Friday" : [],
                "Saturday" : [],
                "Sunday" : []
            }
            json.dump(calendar, f)
            local.CALENDAR_DATA = calendar
            print('[+] New Calendar-data file')

    # Add cogs here
    client.add_cog(VerificationCog(client, local.SERVER_DATA))
    client.add_cog(HelpCog(client))
    client.add_cog(SongsCog(client))
    client.add_cog(CalendarCog(client, local.CALENDAR_DATA))

@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(
                "```Access my commands with:\n"+
                "-help```"
            )
    
    if guild.id not in local.SERVER_DATA:
        local.SERVER_DATA[str(guild.id)] = {
            'verification-channel' : None,
            'verification-role' : None,
            'default-role' : None,
            'server-name' : guild.name
        }

@client.event
async def on_member_join(member):
    await member.send(
        f"Welcome to {member.guild.name}!\n" +\
        "Use `-verify` in a verification channel to be verified."
        )
    
    try:
        role = get(member.guild.roles, name="Unverified")
        await member.add_roles(role)
    except:
        print(f"{member.guild.name} has not set up a verification role")

@client.command(pass_context=True)
async def test(ctx, guild=""):
    if ctx.author.id == 181125845358870528:
        guilds = client.guilds
        
        await ctx.send("Active Servers:")
        for g in [x.name for x in guilds]:
            await ctx.send(g)
        
        server = None
        for g in guilds:
            if g.name == guild:
                await ctx.send("Found!")
                await ctx.send(f"Members: {len(g.members)}")
                for m in g.members:
                    await ctx.send(m.name)
    
    

@client.command(pass_context=True)
async def zoom(ctx, classroom: str):

    classroom = classroom.lower()

    if ctx.guild.id == 439916795554430986:

        classes = [
            [['bio-HL','biology-HL'], "https://us02web.zoom.us/j/"],
            [['econ-HL', 'economics-HL'], 'https://us02web.zoom.us/j/'],
            [['spanish'], 'https://us02web.zoom.us/j/'],
            [['english-HL', 'eng-HL'], 'https://us02web.zoom.us/j/'],
            [['comp-sci-HL', 'compsci-HL','computer-science-hl','cs','cs-HL'], 'https://us02web.zoom.us/j/'],
            [['physics-HL'], ' https://us02web.zoom.us/j/'],
            [['math-SL'], 'https://us02web.zoom.us/j/'],
            [['math-HL'], 'https://us02web.zoom.us/j/'],
            [['english-SL', 'eng-SL'], 'https://us02web.zoom.us/j/'],
            [['ToK', 'ToK-HL', 'theory-of-knowledge', 'theoryofknowledge', 'bushong'], 'https://us02web.zoom.us/j/'],
            [['bus-management', 'buisiness management'], 'https://us02web.zoom.us/j/'],
            [['anatomy', 'anatomy and physiology'], 'https://us02web.zoom.us/j/'],
            [['latin', 'latin-SL'], 'https://us02web.zoom.us/j/4406445896'],
            [['theater', 'theatre', 'theater-HL'], 'https://us02web.zoom.us/j/']
            ]

        for c in classes:
            aliases, link = c
            for alias in aliases:
                if similar(classroom.lower(), alias.lower()) > 0.7:
                    await ctx.send(f"**{aliases[0].title()}**: {link}")
                    break
    else:
        await ctx.send("This server does not have permissions for this command")

@client.command(pass_context=True)
async def bookmark(ctx,*, message=None):

    newMsg = await ctx.send(":scroll: " + ctx.author.name + " has set a bookmark [-bookmark]")
    linkJump = "Message Link: "+str(newMsg.jump_url)
    if message == None:
        await ctx.author.send((":scroll: You have set a bookmark!") + "\nServer: " + ctx.guild.name + " - Channel: " + ctx.channel.name + "\n" + linkJump)
    else:
        await ctx.author.send((":scroll: " + message) + "\nServer: " + ctx.guild.name + " - Channel: " + ctx.channel.name + "\n" + linkJump)
    await ctx.message.delete()

@client.command(pass_context=True)
async def schedule(ctx, new_file : str = None):

    if new_file:
        local.SERVER_DATA[str(ctx.guild.id)]['schedule_file'] = new_file
        await ctx.send(f"Default file changed to: **./images/{new_file}**")
    else:
        if 'schedule_file' in local.SERVER_DATA[str(ctx.guild.id)].keys():
            await ctx.send(file=discord.File(f"./images/{local.SERVER_DATA[str(ctx.guild.id)]['schedule_file']}"))
        else:
            await ctx.send(file=discord.File('./images/schedule.png'))

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, amount, name: discord.User = "None"):
    print(ctx.author.id)
    print(ctx.guild.owner.id)
    if (ctx.author.id != None and ctx.author.id == ctx.guild.owner.id):
        start = time.time()
        if name == "None":

            channel = ctx.message.channel
            await channel.purge(limit=int(amount)+1)

            end = time.time()
            newMsg = await ctx.send("** " + str(amount) + " Messages Deleted**\n`Processing time: " + str(round(end-start,3)) +" seconds`")
            await asyncio.sleep(3)
            await newMsg.delete()
        else:
            count =int(amount)
            channel = ctx.message.channel
            messages = []
            count2 = 0

            messages = await channel.history(limit=101).flatten()
            while (count > 0):
                if messages[count2].author.id == name.id:
                    await messages[count].delete()
                    count -= 1
                count2 += 1

            end = time.time()
            newMsg = await ctx.send("** " + str(amount) + " Messages Deleted**\n`Processing time: " + str(round(end-start,3)) +" seconds`")
            await asyncio.sleep(3)
            await newMsg.delete()
    else:
        msg = await ctx.send("You do not have the necessary permissions required to perform this command!")
        await asyncio.sleep(3)
        await msg.delete()

@client.event
async def on_message(message):

    if message.author.id is client.user.id:
        return    

    '''
    if message.channel.name == local.SERVER_DATA[str(message.guild.id)]["verification-channel"]:
        if message.author.id != client.user.id:
            if 'verify' not in message.content.lower():
                await message.delete()
    '''

    await client.process_commands(message)

client.run(TOKEN, bot=True)

