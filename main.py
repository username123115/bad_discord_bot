import discord
from discord.ext import commands, tasks
import datetime
import random
from secrets import token



eightball_replies = [
    "It is certain",
    "It is decidedly so",
    "Without a doubt",
    "Yes - definitely",
    "As I see it, yes",
    "Most likely",
    "Outlook good",
    "Yes",
    "Signs point to yes",
    "Reply hazy, try again",
    "Ask again later",
    "Better not tell you now",
    "Cannot predict now",
    "Concentrate and ask again",
    "Don't count on it",
    "My reply is no",
    "My sources say no",
    "Outlook not so good",
    "Very doubtful"
]

target_time = (4, 20)
can_say_weed_time = True

client = commands.Bot(command_prefix = "!")

@client.event
async def on_ready():
    print(f"We have logged in as {client}")

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    else:
        if "rickhard" in message.content.lower():
            await message.reply("Hey! I'm Rickhard, but you can call me dick for short")
        if "im bored" in message.content.lower() or "i'm bored" in message.content.lower():
              await message.reply("Hi bored! I'm Rickhard, but you can call me dick for short")
        if "weed" in message.content.lower():
            await message.reply("I luv weed :)")

    await client.process_commands(message)

async def general_say(message = "I luv weed :)", specific_channel = None, guild_name = None):   
    con = False
    for server in client.guilds:
        if guild_name is None:
            con = True
        else:
            if server.name == guild_name:
                con = True
        if con:
            for channel in server.channels:
                if isinstance(channel, discord.TextChannel):
                    if specific_channel is None:
                        send_to = client.get_channel(channel.id)
                        await send_to.send(message)

                    if specific_channel is not None:
                        if channel.name == specific_channel:
                            send_to = client.get_channel(channel.id)
                            await send_to.send(message)

@client.command()
async def ping(ctx):
    await ctx.send("Pong!")

@client.command()
async def get_guilds(ctx):
    await ctx.send(str(client.guilds))

@client.command()
async def gtime(ctx):
    await ctx.send(f"It is now {datetime.datetime.now().hour}: {datetime.datetime.now().minute}")

@client.command()
async def get_channels(ctx):
    for server in client.guilds:
        await ctx.send(f"Server: {server.name}")
        await ctx.send(f"Channels: {[channel.name for channel in server.channels]}")

@client.command()
async def say(ctx, message = "I luv weed : )", channel = None, guild = None):
    await general_say(message, channel, guild)

@client.command()
async def eightball(ctx, message):
    await ctx.reply(random.choice(eightball_replies))

@client.command(name = "random")
async def random_int(ctx, start, end):
    reply = str(random.randint(int(start), int(end)))
    await ctx.reply(reply)


@tasks.loop(seconds = 15)
async def weedtime():
    now = (datetime.datetime.now().hour, datetime.datetime.now().minute)
    global can_say_weed_time
    if now == target_time:
        if can_say_weed_time:
            await general_say("weed time", "memes")
            can_say_weed_time = False
    else:
        can_say_weed_time = True

@client.command()
async def close(ctx):
    await ctx.send("Bravo six, going dark")
    await client.close()

weedtime.start()
client.run(token)