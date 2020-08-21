import asyncio
import time
import discord
from discord.ext import commands

async def play_song(ctx, song, length):
        try:
            channel = ctx.message.author.voice.channel
            await ctx.message.delete()
        except:
            msg = await ctx.send("`You are not in a voice channel!`")
            await asyncio.sleep(3)
            await msg.delete()
            return

        vc = await channel.connect()

        audio_source = discord.FFmpegPCMAudio(f'./sounds/{song}.mp3')
        if not vc.is_playing():
            vc.play(audio_source, after=(None))
            await asyncio.sleep(length) #2
            server = ctx.message.guild.voice_client
            await server.disconnect()

class SongsCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(pass_context=True, aliases=['s','song','sound','sounds'])
    async def songs(self, ctx):
        if ctx.invoked_subcommand in [None]:
            return


    @songs.command(pass_context=True)
    async def bruh(self, ctx):
        await play_song(ctx, 'bruhsound', 2)

    @songs.command(pass_context=True)
    async def fireball(self, ctx):
        await play_song(ctx, 'fireballsound', 2)
    
    @songs.command(pass_context=True)
    async def mrworldwide(self, ctx):
        await play_song(ctx, 'mrworldwidesound', 2)
    
    @songs.command(pass_context=True)
    async def mr305(self, ctx):
        await play_song(ctx, 'mr305sound', 3)
    
    @songs.command(pass_context=True)
    async def ironman(self, ctx):
        await play_song(ctx, 'americadoesitsound', 9)
    
    @songs.command(pass_context=True)
    async def helicopter(self, ctx):
        await play_song(ctx, 'helicoptersound', 17)

    @songs.command(pass_context=True)
    async def strike(self, ctx):
        await play_song(ctx, 'wiibowling', 4)
    
    @songs.command(pass_context=True)
    async def yodadeath(self, ctx):
        await play_song(ctx, 'yodadeath', 2)

    @songs.command(pass_context=True)
    async def minikit(self, ctx):
        await play_song(ctx, 'minikit', 4)

    @songs.command(pass_context=True)
    async def jarjar(self, ctx):
        await play_song(ctx, 'jarjar', 4)

    @songs.command(pass_context=True)
    async def knock(self, ctx):
        await play_song(ctx, 'knock', 20)
    
    @songs.command(pass_context=True)
    async def droiddeath(self, ctx):
        await play_song(ctx, 'droiddeath', 4)
    
    @songs.command(pass_context=True)
    async def dejavu(self, ctx):
        await play_song(ctx, 'dejavu', 28)

    @songs.command(pass_context=True)
    async def nice(self, ctx):
        await play_song(ctx, 'nice', 7) 

    @songs.command(pass_context=True)
    async def koolaid(self, ctx):
        await play_song(ctx, 'koolaid', 2.2)

    @songs.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def windowsxp(self, ctx):
        await play_song(ctx, 'windowsmeme', 4)
