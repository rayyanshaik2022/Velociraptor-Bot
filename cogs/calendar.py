import asyncio
import time
import discord
from discord.ext import commands
import datetime

class CalendarCog(commands.Cog):
    def __init__(self, client, calendar):
        
        self.client = client
        self.calendar = calendar

        self.week = [
            "monday", "tuesday", "wednesday", "thursday", "friday",
            "saturday", "sunday"
        ]

    @commands.group(pass_context=True, aliases=['c'])
    async def calendar(self, ctx):

        if ctx.invoked_subcommand in [None]:
            c = 0
            embed = discord.Embed(title="Calendar Help Menu", description="", color=0x03fcba)
            for key in self.calendar:
                desc = ['```','```']
                for work in self.calendar[key]:
                    desc.insert(1, work)
                    c += 1
                if self.calendar[key] != []:
                    embed.add_field(name=key.title(), value="\n".join(desc), inline=False)
            embed.set_footer(text="Requested by " + str(ctx.author.name),
                icon_url=ctx.author.avatar_url)
            if c == 0:
                embed.add_field(name="No work added.", value="--------", inline=False)
            await ctx.send("", embed=embed)

    @calendar.command(pass_context=True)
    async def add(self, ctx, day, *, work : str):
        
        if len(work) > 120:
            work = "Invalid"

        if day.lower() == "today":
            weekday = self.week[datetime.date.today().weekday()].title()
            if work not in self.calendar[weekday]:
                self.calendar[weekday].append(work)
            await ctx.send(f"```{work}```\nAdded to {day.lower().title()}'s homework.")
        elif day.lower() in self.week:
            self.calendar[day.lower().title()].append(work)
            await ctx.send(f"```{work}```\nAdded to {day.lower().title()}'s homework.")

    @calendar.command(pass_context=True)
    async def remove(self, ctx, day, *, work : str):

        if day.lower() == "today":
            weekday = self.week[datetime.date.today().weekday()].title()
            if work in self.calendar[weekday]:
                self.calendar[weekday].remove(work)
                await ctx.send(f"```{work}```\nRemoved from {day.lower().title()}'s homework.")
            else:
                await ctx.send(f"Could not find\n```{work}```\nin {day}.")
        elif day.lower() in self.week:
            if work in self.calendar[day.lower().title()]:
                self.calendar[day.lower().title()].remove(work)
                await ctx.send(f"```{work}```\nRemoved from {day.lower().title()}'s homework.")
            else:
                await ctx.send(f"Could not find\n```{work}```\nin {day}.")
        else:
            await ctx.send(f"Could not find\n```{work}```\nin {day}.")

    @calendar.command(pass_context=True)
    async def clear(self, ctx, day):

        if day.lower() == "today":
            weekday = self.week[datetime.date.today().weekday()].title()
            self.calendar[weekday] = []
            await ctx.send("Cleared today's school work")
        elif day.lower() in self.week:
            self.calendar[day.lower().title()] = []
            await ctx.send(f"Cleared {day.lower().title()}'s school work")
        elif 'all':
            for day in self.week:
                self.calendar[day.lower().title()] = []
            await ctx.send("Cleared the week's school work")


    @calendar.command(pass_context=True)
    async def help(self, ctx):
        desc = [
                "```General Format:\n-c add/remove date item\n-c clear date/all```",
                "```Dates: Monday-Sunday, Today```",
                "```",
                "Examples:",
                '-c add today Physics: read 8-9',
                '-c remove Saturday Math test: hard',
                '-c clear all'
                "```"
            ]

        embed = discord.Embed(title="Calendar Help Menu", description="\n".join(desc), color=0x03fcba)
        embed.set_footer(text="Requested by " + str(ctx.author.name),
                icon_url=ctx.author.avatar_url)
        await ctx.send("", embed=embed)
