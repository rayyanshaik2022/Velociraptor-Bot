import asyncio
import time
import discord
from discord.ext import commands
from discord.utils import get

class VerificationCog(commands.Cog):
    def __init__(self, client, server_data):
        
        self.client = client
        self.SERVER_DATA = server_data

    @commands.group(pass_context=True, aliases=['verification','v'])
    async def verify(self, ctx):
        # Establishes 'verify' and aliases as the main command
        
        if ctx.invoked_subcommand in [None]:
            
            if str(ctx.guild.id) in self.SERVER_DATA:
                if str(ctx.guild.id) in self.SERVER_DATA:
                    if ctx.message.channel.name == self.SERVER_DATA[str(ctx.guild.id)]['verification-channel']:
                        counter = 0
                        async for message in ctx.message.channel.history(limit=50):
                            if (message.author.id == ctx.author.id):
                                counter += 1
                        
                        if counter > 1:
                            await ctx.message.author.send(
                                f"Please do not spam #{ctx.message.channel.name}"
                                )
                            await ctx.message.delete()
                        else:
                            await ctx.message.author.send(
                                "Your verification is now pending"
                                )
                            
                            if self.SERVER_DATA[str(ctx.guild.id)] == None:
                                self.SERVER_DATA[str(ctx.guild.id)] = ctx.guild.name
                    else:
                        if self.SERVER_DATA[str(ctx.guild.id)]['verification-channel'] in [None,'None']:
                            await ctx.send("This server has not established a verification channel.")
                        else:
                            await ctx.author.send(f"Please use #{self.SERVER_DATA[str(ctx.guild.id)]['verification-channel']}")
                            await ctx.message.delete()
                else:
                    await ctx.send("This server has not established a verification channel.")
            else:
                await ctx.send("This server has not established a verification channel.")
                self.SERVER_DATA[str(ctx.guild.id)] = {
                    'verification-channel' : None,
                    'verification-role' : None,
                    'default-role' : None,
                    'server-name' : None
                }


    @verify.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def set_channel(self, ctx):

        self.SERVER_DATA[str(ctx.guild.id)]['verification-channel'] = ctx.message.channel.name
        await ctx.send(f"Verification channel now set to #{ctx.channel.name}")

    @verify.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def default_role(self, ctx, role: discord.Role):
        if role == None:
            return
        
        self.SERVER_DATA[str(ctx.guild.id)]['default-role'] = role.name
    
    @verify.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def new_role(self, ctx, role: discord.Role):
        if role == None:
            return
        
        self.SERVER_DATA[str(ctx.guild.id)]['verification-role'] = role.name

    @verify.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def accept(self, ctx, user: discord.User):
        
        if ctx.message.channel.name == self.SERVER_DATA[str(ctx.guild.id)]['verification-channel']:
            if user != None:
                async for message in ctx.message.channel.history(limit=50):
                    if message.author.id == user.id:
                        await  message.delete()

                member = ctx.guild.get_member(user.id)
                
                if self.SERVER_DATA[str(ctx.guild.id)]['default-role'] != None:
                    try:
                        await member.remove_roles(get(ctx.guild.roles, name=self.SERVER_DATA[str(ctx.guild.id)]['default-role']))
                    except Exception as e:
                        print(e)
                
                if self.SERVER_DATA[str(ctx.guild.id)]['verification-role'] != None:
                    try:
                        role = get(ctx.guild.roles, name=self.SERVER_DATA[str(ctx.guild.id)]['verification-role'])
                        await member.add_roles(role)
                    except Exception as e:
                        print(e)

                await user.send("You have been verified")
   
    @verify.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def deny(self, ctx, user: discord.User):
        member = ctx.guild.get_member(user.id)
        await member.send(content="Your verification request was denied.")
        await ctx.guild.kick(member)


