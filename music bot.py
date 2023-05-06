import discord
from discord.ext import commands
import youtube_dl
import os

bot = commands.Bot(command_prefix='.')


@bot.command()
async def play(ctx, *, query):
    voice_channel = ctx.author.voice.channel
    if not voice_channel:
        await ctx.send("You need to be in a voice channel to play music!")
        return
    
    await voice_channel.connect()
    query = query.replace(" ", "+")
    url = f"https://www.youtube.com/results?search_query={query}"
    ydl_opts = {'format': 'bestaudio', 'quiet': True}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=False)['entries'][0]
        audio_url = result['url']
        title = result['title']
    ctx.voice_client.play(discord.FFmpegPCMAudio(audio_url), after=lambda e: print(f"Finished playing: {title}"))
    await ctx.send(f"Now playing: {title}")

bot.run("YOUR_BOT_TOKEN")