import discord, asyncio, os
from discord.channel import VoiceChannel
from discord.ext import commands
from discord.ext.commands import Bot
from youtube_dl import YoutubeDL
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from discord.utils import get
from discord import FFmpegPCMAudio
import asyncio
import time

import youtube_dl

game = discord.Game("저울질")
bot = commands.Bot(command_prefix = '-', status = discord.Status.online, activity = game)

@bot.event
async def on_ready():
    print('다음으로 로그인합니다: ')
    print(bot.user.name)
    print('connection was succesful')
    await bot.change_presence(status = discord.Status.online, activity = None)
    
@bot.command()
async def 들어와(ctx):
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("채널에 유저가 없잖아")
            
@bot.command()
async def 나가(ctx):
    try:
        await vc.disconnect()    
    except:
        await ctx.send("이미 그 채널에 없음;;")
        
@bot.command()
async def 깝치네(ctx):
    await ctx.send("어쩔티비 ㅋㅋ")
    
@bot.command()
async def URL재생(ctx, *, url):
    YDL_OPTIONS = {'format': 'bestaudio','noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    if not vc.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        await ctx.send(embed = discord.Embed(title= "노래 나옴 ㅋㅋ", description = "지금 " + url + "을(를)재생중~.", color = 0x00ff00))
    else:
        await ctx.send("노래가 이미 재생되고 있습니다!")
        
@bot.command()
async def 재생(ctx, *, msg):
    if not vc.is_playing():
        global entireText
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            
        chromedriver_dir = "C:\ChromeDriver\chromedriver.exe"
        driver = webdriver.Chrome(chromedriver_dir)
        driver.get("https://www.youtube.com/results?search_query="+msg+"+lyrics")
        source = driver.page_source
        bs = bs4.BeautifulSoup(source, 'lxml')
        entire = bs.find_all('a', {'id': 'video-title'})
        entireNum = entire[0]
        entireText = entireNum.text.strip()
        musicurl = entireNum.get('href')
        url = 'https://www.youtube.com'+musicurl 

        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        await ctx.send(embed = discord.Embed(title= "노래 나옴 ㅋㅋ", description = "지금 " + entireText + "을(를)재생중~.", color = 0x00ff00))
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
    else:
        await ctx.send("이미 노래가 재생 중이라 노래를 재생할 수 없어!")
        
@bot.event
async def on_message(message):
    if message.author.bot:
        return None
    if message.content.endswith("ㅋ") or message.content.endswith("z"):
        file = discord.File("C:\\Users\\82104\\Videos\\Captures\\rupy.png")
        await message.channel.send(file = file)
        await message.channel.send("개웃기네 ㅋ")
        
    if message.content.endswith("ㄱ"):
        file = discord.File("C:\\Users\\82104\\Videos\\Captures\\tenor.gif")
        await message.channel.send(file = file)
        await message.channel.send("고!")

bot.run('OTI0ODg5Mjc4MjMwNzE2NDM2.YclIQw.NfyaydhK9uigfOHXyBNXnFmuWf8')
