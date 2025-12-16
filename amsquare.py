#start


#imports
import discord
from discord.ext import commands
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
from dotenv import load_dotenv


#load keys env file
load_dotenv()

#Initialize Firebase
cred = credentials.Certificate((json.loads(os.getenv("firebase_key"))))
firebase_admin.initialize_app(cred)
db = firestore.client()
users_ref = db.collection("users")

#bot setup
ints = discord.Intents.default()
ints.messages = True
ints.message_content = True
ints.guilds = True
ints.members = True

bot = commands.Bot(command_prefix = "*", intents = ints)


#on ready event
@bot.event
async def on_ready():
    #set bot presence
    await bot.change_presence(
        status = discord.Status.online, 
        activity = discord.Game(name = "Being Coded")
    )
    print("Bot Connected")

    #send message to specific channel
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
        
          
#XP system    
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    userid = str(message.author.id)
    userdoc = users_ref.document(userid)

    data = userdoc.get().to_dict()
    if data is None:
        data = {"xp": 0,"level":1}
    
    data["xp"] = data["xp"] + 10
    
    xp = data["xp"]
    level = data["level"]
    xpneed = level * 100

    #check for level up
    if xp >= xpneed:
        data["level"] = data["level"] + 1
        data["xp"] = xp - xpneed
        
        await message.channel.send(f"**{message.author.name} leveled up to level {data["level"]}!**")
        
    userdoc.set(data)
        
    await bot.process_commands(message)
            

#level command
@bot.command()
async def level(context, member: discord.Member = None):
    #get member info
    member  = member or context.author
    userid = str(member.id)
    
    userdoc = users_ref.document(userid).get()
    data = userdoc.to_dict()

    if data is None:
        return await context.send(f"{member.name} has no XP yet.")
    
    xp = data["xp"]
    level = data["level"]
    
    #send level and xp info
    await context.send(
        f"**{member.name}**\n"
        f"Level: **{level}**\n"
        f"XP: **{xp}**"
)


#leaderboard command
@bot.command()
async def leaderboard(context):

    xpref = db.collection("users")

    docs = xpref.stream()
    data = []

    for doc in docs:
        userdata = doc.to_dict()
        data.append((doc.id,userdata))

    if len(data) == 0:
        return await context.send("No XP data available yet.")

    #sort users by xp
    sortedusers = sorted(data, key = lambda x: x[1]["xp"], reverse = True)
    
    top10 = sortedusers[:10]

    msg = "__**AMsquare Leaderboard**__\n\n"
    
    #build leaderboard message
    rank = 1
    for (userid,data) in top10:
        user = await bot.fetch_user(int(userid))
        xp = data["xp"]
        level = data["level"]
        
        msg = msg + f"{rank}. {user.name} — Level {level}, {xp} XP\n"
        rank = rank + 1
        
    await context.send(msg)


#run 
bot.run(os.getenv('discord_token'))


#end
