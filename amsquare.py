#start



import discord
from discord.ext import commands
import json
import os



ints = discord.Intents.default()
ints.messages = True
ints.message_content = True
ints.guilds = True
ints.members = True

bot = commands.Bot(command_prefix = "*", intents = ints)



@bot.event
async def on_ready():
    await bot.change_presence(
        status = discord.Status.online, 
        activity = discord.Game(name = "Being Coded")
    )
    print("Bot Connected")

    try:
        channel = bot.get_channel(1449705870698090629)

        if channel is None:
            channel = await bot.fetch_channel(1449705870698090629)
            if channel is None:
                print("Channel not found")
            else:
                return
        message = await channel.send("AMsquare, squaring as always!")
        await message.add_reaction("🤖")

    except Exception as e:
        print(f"Error: {e}")
        
        
        
xpfile = "xp.json"  
if os.path.exists(xpfile):
    with open(xpfile, "r") as F:
        xpdata = json.load(F)   
else:
    xpdata = {}
        
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    userid = str(message.author.id)
    
    if userid not in xpdata:
        xpdata[userid] = {"xp": 0, "level": 1}
        
    xpdata[userid]["xp"] = xpdata[userid]["xp"] + 10
    
    xp = xpdata[userid]["xp"]
    level = xpdata[userid]["level"]
    xpneed = level * 100
    
    if xp >= xpneed:
        xpdata[userid]["level"] = xpdata[userid]["level"] + 1
        xpdata[userid]["xp"] = xpdata[userid]["xp"] - xpneed
        
        await message.channel.send(f"**{message.author.name} leveled up to level {xpdata[userid]["level"]}!**")
        
    with open(xpfile, "w") as F:
        json.dump(xpdata, F)
        
    await bot.process_commands(message)
            


@bot.command()
async def level(context, member: discord.Member = None):
    member  = member or context.author
    userid = str(member.id)
    
    if userid not in xpdata:
        return await context.send(f"{member.name} has no XP yet.")
    
    xp = xpdata[userid]["xp"]
    level = xpdata[userid]["level"]
    
    await context.send(
        f"**{member.name}**\n"
        f"Level: **{level}**\n"
        f"XP: **{xp}**"
)
    


@bot.command()
async def leaderboard(context):
    if len(xpdata) == 0:
        return await context.send("No XP data available yet.")
    
    sortedusers = sorted(xpdata.items(), key = lambda x: x[1]["xp"], reverse = True)
    
    top10 = sortedusers[:10]

    msg = "__**AMsquare Leaderboard**__\n\n"
    
    rank = 1
    for (userid,data) in top10:
        user = await bot.fetch_user(int(userid))
        xp = data["xp"]
        level = data["level"]
        
        msg = msg + f"{rank}. {user.name} — Level {level}, {xp} XP\n"
        rank = rank + 1
        
    await context.send(msg)


bot.run('token')



#end
