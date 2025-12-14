#start

import discord
from discord.ext import commands

ints = discord.Intents.default()
ints.messages = True
ints.message_content = True
ints.guilds = True
ints.members = True

bot = commands.Bot(command_prefix = "$", intents = ints)

@bot.event
async def on_ready():
    await bot.change_presence(
        status = discord.Status.online, 
        activity = discord.Game(name = "Sleeping ZZZ")
    )
    print("Bot Connected")

    try:
        channel = bot.get_channel(1449705870698090629)

        if channel is None:
            channel = await bot.fetch_channel(1449705870698090629)
        elif channel is not None:
            message = await channel.send("AMsquare, squaring as always!")
            await message.add_reaction("🤖")
        else:
            print("Channel not found")

    except Exception as e:
        print(f"Error: {e}")

bot.run('token')

#end
