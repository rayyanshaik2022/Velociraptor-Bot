import asyncio
import time
import discord
from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, client):
        
        self.client = client

    @commands.group(pass_context=True)
    async def help(self, ctx):

        if ctx.invoked_subcommand in [None]:
            desc = [
                "```-help admin```",
                "```-help songs```",
                "```",
                "-zoom (class)",
                "-bookmark (message)",
                "-schedule"
                "```"
            ]

            embed = discord.Embed(title="Help Menu", description="\n".join(
            desc), color=0x03fcba)
            embed.set_footer(text="Requested by " + str(ctx.author.name),
                        icon_url=ctx.author.avatar_url)
            await ctx.send("", embed=embed)

    @help.command(pass_context=True)
    async def admin(self, ctx):
        desc = [
                "```",
                "-clear (# of messages)",
                "-verify set_channel (channel name)",
                "-verify default_role (@role)",
                "-verify new_role (@role)",
                "-verify accept (@user)",
                "-verify deny (@user)"
                "```"
            ]
        
        embed = discord.Embed(title="Help Menu | Admin", description="\n".join(
            desc), color=0x03fcba)
        embed.set_footer(text="Requested by " + str(ctx.author.name),
            icon_url=ctx.author.avatar_url)
        await ctx.send("", embed=embed)

    @help.command(pass_context=True)
    async def songs(self, ctx):

        cmd_names = [
            'bruh','fireball','mrworldwide',
            'mr305','ironman','helicopter',
            'windowsxp','strike',
            'yodadeath','minikit','jarjar',
            'knock','droiddeath','dejavu',
            'nice','koolaid'
        ]
        desc = [
            "```",
            "-s (sound name)"
            "```",
            "```",
            "```"
        ]
        for item in cmd_names:
            desc.insert(4, item)
        
        embed = discord.Embed(title="Help Menu | Sounds", description="\n".join(
        desc), color=0x03fcba)
        embed.set_footer(text="Requested by " + str(ctx.author.name),
                     icon_url=ctx.author.avatar_url)
        await ctx.send("", embed=embed)