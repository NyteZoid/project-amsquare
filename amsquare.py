
import discord

ints = discord.Intents.default()
ints.messages = True
ints.message_content = True

client = discord.Client(intents = ints)

@client.event
async def on_ready():
    await client.change_presence(
        status = discord.Status.online, 
        activity = discord.Game(name="Sleeping ZZZ")
    )
    print("Bot Connected")

    try:
        channel = client.get_channel(1449705870698090629)

        if channel is None:
            channel = await client.fetch_channel(1449705870698090629)
        elif channel is not None:
            message = await channel.send("AMsquare, squaring as always!")
            await message.add_reaction("🤖")
        else:
            print("Channel not found")

    except Exception as e:
        print(f"Error: {e}")

client.run('TOKEN')

#end
