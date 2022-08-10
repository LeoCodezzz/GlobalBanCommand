import discord
import json
from pathlib import Path
from discord.ext import commands

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f'{cwd}\n-----')

bot = commands.Bot(command_prefix = "[CHANGE ME]")
bot.bannedusers = []

@bot.event
async def on_ready():
    print('DeveloperProtection is online.')
    while True:
        await bot.change_presence(status=discord.Status.online, activity=discord.Activity(
        type=discord.ActivityType.watching, name=f"[CHANGE ME!(STATUS)]"
    ))
    await asyncio.sleep(60)


#COMMANDS

@bot.command()
@commands.has_role()
async def ban(ctx, member: discord.User):
    channel2 = ctx.bot.get_channel()
    channel = ctx.bot.get_channel()

    embed = discord.Embed(title = f'Banning {member}...')
    await ctx.send(embed = embed)
    await ctx.send('What is the reason for this ban?')
    reason = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)

    embed2 = discord.Embed(title = 'Please give proof of this ban. Convert image to a link.')
    await ctx.send(embed = embed2)
    proof = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)

    embed3 = discord.Embed(title = 'Ban Output', description = f'User: `{member}`\nReason: `{reason.content}`')
    embed3.set_image(url = proof.content)
    await ctx.send(embed = embed3)
    await ctx.send('Is this correct? `Y / N`')
    confirm = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    if confirm.content == 'Y' or 'y':

        embed4 = discord.Embed(title = 'Member Banned!')
        embed4.add_field(name = 'Banned User:', value = f'{member} [`{member.id}`]', inline = False)
        embed4.add_field(name = 'Banned By', value = f'{ctx.author} [`{ctx.author.id}`]', inline = False)
        embed4.add_field(name = 'Reason', value = f'{reason.content}', inline = False)
        embed4.set_image(url = proof.content)
    
        await channel2.send(f'**New Banned User**```User: {member}\nUser ID: {member.id}\nReason: {reason.content}\nProof: {proof.content}```')

        bot.bannedusers.append(member.id)
        data = read_json("bans")
        data["bannedusers"].append(member.id)
        write_json(data, "bans")

        await ctx.send('Member has been banned.')
        await channel.send(embed = embed4)
        for guild in bot.guilds:
    	    await guild.ban(member)


@bot.command()
@commands.has_role()
async def whitelist(ctx, member: discord.User):
    channel = ctx.bot.get_channel()
    channel2 = ctx.bot.get_channel()

    for guild in bot.guilds:
        await guild.unban(member)
    await ctx.send(f'**{member}** has been whitelisted.')

    await channel.send(f'**New Whitelisted User**```User: {member}\nUser ID: {member.id}```')

    embed = discord.Embed(title = 'Member Whitelisted!', description = f'User: `{member.name}`\nUser ID: `{member.id}`')
    await channel2.send(embed = embed)


@bot.command()
async def report(ctx, member: discord.User):
    channel = ctx.bot.get_channel()
    guild = ctx.guild

    embed = discord.Embed(title = f'Reporting {member}...')
    await ctx.send(embed = embed)
    await ctx.send('What is the reason for this report?')
    reason = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)

    embed2 = discord.Embed(title = 'Please give proof of this report. Convert image to a link.')
    await ctx.send(embed = embed2)
    proof = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)

    embed3 = discord.Embed(title = f"{ctx.author.name}'s Report")
    embed3.add_field(name = 'Reported User:', value = f'[`{member.name}`]', inline = False)
    embed3.add_field(name = 'User Discriminator:', value = f'[`#{member.discriminator}`]', inline = False)
    embed3.add_field(name = 'Reason:', value = f'{reason.content}', inline = False)
    embed3.add_field(name = 'Guild:', value = f'`{ctx.guild.name}`', inline = False)
    embed3.add_field(name = 'Proof:', value = 'Proof Below', inline = False)
    embed3.set_image(url = proof.content)

    await channel.send(embed = embed3)
    await ctx.send(f'{ctx.author.mention} Your report has been sent!')


#JSON
def read_json(filename):
    with open(f'{cwd}/config/{filename}.json', 'r') as file:
        data = json.load(file)
    return data

def write_json(data, filename):
    with open(f'{cwd}/config/{filename}.json', 'w') as file:
        json.dump(data, file, indent = 4)

bot.run('')