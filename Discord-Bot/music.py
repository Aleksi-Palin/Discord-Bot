import discord
from discord.ext import commands
import youtube_dl
import asyncio
#from queue import Queue
from collections import deque

#ei valmis koita korjaa miten saat tiedettyy missä biisisssä ollaan
#miten tietää onko soitettu kerran että meneekä queue



FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn'}

YDL_OPTIONS = {'format': "bestaudio",
            'quiet': True,
            'no_warnings':True,
            'default_search': 'auto',
            'postprocessors':[{
              'key': 'FFmpegExtractAudio',
              'preferredcodec': 'mp3',
              'preferredquality': '192',
            }],}



#create loop for all songs in queue
#own list for every server not all playing from same list




async def start_playing(self,ctx,queue):
      client = ctx.voice_client
      
      print(len(queue))
      
      while True:
        if(client.is_playing() == True):
          print("still Playing")
          return
        #print("not playing")

        url = queue.popleft()

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2,**FFMPEG_OPTIONS)
            client.play(source,after=lambda e: print('Player error: %s' % e) if e else None)

            await ctx.send("Now Playing!\n" + url)
            #print(len(queue))
            print(info['duration'])
            await asyncio.sleep(info['duration'])
            

            #check if bot is disconnected

        print("video ended")
        if(len(queue) == 0):
          break
      
  
    
class music(commands.Cog):
  queue = deque()

  def __init__(self,client):  
      self.client = client
      
  @commands.command(name="join")
  async def join(self,ctx):
    if ctx.author.voice is None:
      await ctx.send("You're not in a voice channel!")
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
      await voice_channel.connect()
      music.queue.clear()
      await ctx.send("Joined the voice channel!")
    else:
      await ctx.voice_client.move_to(voice_channel)

  @commands.command(name="leave")
  async def leave(self,ctx):
    
    await ctx.voice_client.disconnect()
    
    await ctx.send("I left the voice channel")

  @commands.command(name="stop")
  async def stop(self,ctx):
    ctx.voice_client.stop()
    await ctx.send("Sound Stopped")
    
  @commands.command(name="pause")
  async def pause(self,ctx):
    ctx.voice_client.pause()
    await ctx.send("Sound Paused")

  @commands.command(name="resume")
  async def resume(self,ctx):
    ctx.voice_client.resume()
    await ctx.send("Sound Resumed")
  
  @commands.command(name="skip")
  async def skip(self,ctx):
    #skip
    ctx.voice_client.stop()
    await start_playing(self,ctx,music.queue)
    ctx.send("Song skipped")


  @commands.command(name="queue")
  async def getqueue(self,ctx):
    await ctx.send("Queue:\n" + str(music.queue))
    #await ctx.send(queue)

  @commands.command(name="play") 
  async def play(self, ctx, url):

    vc = ctx.voice_client
    
    voice_channel = ctx.author.voice.channel  

    if(vc is None):
      await voice_channel.connect()
      music.queue.clear()
      vc = ctx.voice_client
    #print(vc)

    try:
      if(vc.is_playing() == False):
        music.queue.append(url)
        await start_playing(self,ctx,music.queue)
      elif(vc.is_playing() == True):
        music.queue.append(url)
        await ctx.send("Added to queue") 
      elif(vc.is_paused() == True):
        music.queue.append(url)
        await ctx.send("Added to queue")
      

    except:
        await ctx.send("Somenthing went wrong - please try again later!")
    
    

def setup(client):
 client.add_cog(music(client))


  