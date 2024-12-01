import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio  # 비동기 작업을 위해 추가

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True  # 음성 채널 관련 이벤트를 처리하기 위해 추가

bot = commands.Bot(command_prefix='$', intents=intents)

cant_defuse = True
defuse = False

@bot.command()
async def 설치(ctx):
    if ctx.author.voice:
        voice_channel = ctx.author.voice.channel
        spike_plant_voice = await voice_channel.connect()

        audio_file = "spike_plant.mp3"
        if os.path.exists(audio_file):
            FFMPEG_OPTIONS = {
                'options': '-vn'
            }
            def plant(error):
                if defuse == False:
                    asyncio.run_coroutine_threadsafe(폭발(ctx), bot.loop)
                    
            spike_plant_voice.play(discord.FFmpegPCMAudio(audio_file, **FFMPEG_OPTIONS), after = plant)
            asyncio.run_coroutine_threadsafe(timer(ctx), bot.loop)
            await ctx.send(f"{voice_channel.name}에서 설치합니다!")

    else:
        await ctx.send("스파이크를 두고왔어...")

@bot.command()
async def 해체(ctx):
    if ctx.author.voice:
        if cant_defuse:
            asyncio.run_coroutine_threadsafe(틱(ctx), bot.loop)
        else :
            await ctx.send("시간이 없어...")
            
    else:
        await ctx.send("해체 키트를 두고왔어...")

async def 폭발(ctx):
    if ctx.author.voice:
        voice_channel = ctx.author.voice.channel
        members = voice_channel.members

        for member in members:
            if member != ctx.guild.me:
                await member.move_to(None) 
                await ctx.send(f'{member.display_name}님이 죽었습니다.')
        
        if ctx.voice_client and ctx.voice_client.is_connected():
                await ctx.voice_client.disconnect()

async def 틱(ctx):
    global defuse
    await asyncio.sleep(1)
    await ctx.send("...1")
    await asyncio.sleep(1)
    await ctx.send("...2")
    await asyncio.sleep(1)
    await ctx.send("...3")
    await asyncio.sleep(1)
    await ctx.send("...4")
    await asyncio.sleep(1)
    await ctx.send("...5")
    await asyncio.sleep(1)
    await ctx.send("...6")
    await asyncio.sleep(1)
    await ctx.send("...7")
    await ctx.send("해체 성공!")
    defuse = True
    if ctx.voice_client and ctx.voice_client.is_connected():
                await ctx.voice_client.disconnect()

    
    if ctx.voice_client and ctx.voice_client.is_connected():
        asyncio.run_coroutine_threadsafe(ctx.voice_client.disconnect(), bot.loop)

async def timer(ctx):
    global cant_defuse
    await asyncio.sleep(30)
    cant_defuse = False
     
bot.run(TOKEN)