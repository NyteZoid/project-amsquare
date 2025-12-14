#start

import discord 

client = discord.Client()

@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.online, 
        activity=discord.Game(name="x", type=3)
    )
    print("Bot Connected")

    channel = client.get_channel(x)
    if channel is not None:
        message = await channel.send("x")
        await message.add_reaction("x")
    else:
        print("Channel not found")

client.run('token')

#end
