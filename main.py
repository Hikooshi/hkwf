from config import settings
import discord
from discord.ext import commands
import requests

bot = commands.Bot(command_prefix=settings["prefix"], intents=discord.Intents.all())

def getResponse(n):
    options = [
        "cetusCycle",
        "earthCycle"
    ]
    url = f"https://api.warframestat.us/pc/{options[n]}?language=ru"
    return requests.get(url).json()

@bot.command()
async def hello(ctx):
    author = ctx.message.author
    await ctx.send(f"test {author.mention}")

@bot.command()
async def cetus(ctx):
    response = getResponse(0)
    dayTime = ["Ночь", "День"]
    toDayTime = ["До наступления дня", "До наступления ночи"]
    isDay = response["isDay"]
    timeLeft = response["timeLeft"]
    result = f"Сейчас на Цетусе {dayTime[isDay]}. {toDayTime[isDay]} еще {timeLeft}!"
    embed = discord.Embed(
        description=result,
        color=0x0000FF
    )
    await ctx.send(embed=embed)

@bot.command()
async def earth(ctx):
    response = getResponse(1)
    dayTime = ["Ночь", "День"]
    toDayTime = ["До наступления дня", "До наступления ночи"]
    isDay = response["isDay"]
    timeLeft = response["timeLeft"]
    result = f"Сейчас на Земле (обычные миссии) {dayTime[isDay]}. {toDayTime[isDay]} еще {timeLeft}!"
    embed = discord.Embed(
        description=result,
        color=0x0000FF
    )
    await ctx.send(embed)

bot.run(settings["token"])