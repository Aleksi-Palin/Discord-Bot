#imports
#import os
#import sys
#import discord
from Keep_alive import keep_alive
from discord.ext import commands
import variables
import weather
import twitter
import quote
import music
import Translator

#specify cogs
cogs = [music]

#set bot variable and prefix
bot = commands.Bot(command_prefix = '.')

#check for all cogs
for i in range(len(cogs)):
  cogs[i].setup(bot)

#start bot
@bot.event
async def on_ready():
  print('we have logged in as {0.user}'.format(bot))

#read text channels function
# @bot.event
# async def on_message(message):
#   await bot.process_commands(message)
#   if message.author == bot.user:
#     return

@bot.command(name="commands")
async def help(message):
  await message.channel.send("COMMANDS\n.weather <city>\n.tweet <username>")

@bot.command(name="Invite")
async def inv(message):
  await message.channel.send("https://discordapp.com/oauth2/authorize?&client_id=867515608379818035&permissions=8&scope=bot")

@bot.command(name="quote")
async def getquote(message):
  await message.channel.send(quote.get_quote())

#get latest weather update from chosen city
@bot.command(name="weather")
async def getweather(message,city):
  await message.channel.send(weather.get_weather(city))

#get newest tweet from chosen user
@bot.command(name="tweet")
async def newtweet(message,username):
  pull_tweet= twitter.get_tweet(username)
  user = str(username)
  await message.channel.send("Latest tweet or replie from "+user+"\n -"+pull_tweet) 
  
@bot.command(name="translate")
async def translate(message,text,lang):
  await message.channel.send(Translator.translate(text,lang))

#https server what is pinged every 5 minutes
keep_alive()

#run the bot
bot.run(variables.BOT_TOKEN)

