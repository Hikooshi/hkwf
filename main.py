from config import settings
import discord
from discord.ext import commands
import requests

bot = commands.Bot(command_prefix=settings["prefix"], help_command=None, intents=discord.Intents.all())

options = [
        "cetusCycle",
        "earthCycle",
        "cambionCycle",
        "arbitration",
        "archonHunt",
        "constructionProgress"
    ]

dayTime = ("Ночь", "День")
toDayTime = ("До наступления дня", "До наступления ночи")
vf = {"vome" : "Воум", "fass" : "Фэз"}
enemies = {"Orokin" : "Орокин",
               "Corrupted" : "Порабощенные",
               "Infested" : "Заражённые",
               "Corpus" : "Корпус",
               "Grineer" : "Гринир",
               "Narmer" : "Нармер"}

def getResponse(n):
    url = f"https://api.warframestat.us/pc/{options[n]}?language=ru"
    return requests.get(url).json()

def getArch(archwing):
    if archwing:
        return "нужен"
    return "не нужен"

@bot.command()
async def cetus(ctx):
    response = getResponse(0)
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
    isDay = response["isDay"]
    timeLeft = response["timeLeft"]
    result = f"Сейчас на Земле (обычные миссии) {dayTime[isDay]}. {toDayTime[isDay]} еще {timeLeft}!"
    embed = discord.Embed(
        description=result,
        color=0x0000FF
    )
    await ctx.send(embed=embed)

@bot.command()
async def camb(ctx):
    response = getResponse(2)
    timeLeft = response["timeLeft"]
    wrm = response["active"]
    result = f"Сейчас на Камбионийском дрейфе {vf[wrm]}. Еще {timeLeft}!"
    embed = discord.Embed(
        description=result,
        color=0x0000FF
    )
    await ctx.send(embed=embed)

@bot.command()
async def arbi(ctx):
    response = getResponse(3)
    sharkwing = response["sharkwing"] and "ДА" or "НЕТ"
    result = f"Тип арбитража: {response['type']}. Противник: {enemies[response['enemy']]}. Локация: {response['node']}. " \
             f"Арчвинг {getArch(response['archwing'])}. Под водой: {sharkwing}"
    embed = discord.Embed(
        description=result,
        color=0x0000FF
    )

    await ctx.send(embed=embed)

@bot.command()
async def hunt(ctx):
    response = getResponse(4)
    missions = response["missions"]
    embed = discord.Embed(
        title="Охота на Архонта",
        color=0x0000FF
    )
    embed.add_field(name=missions[0]["type"], value=missions[0]["node"] + "\n\nАрчвинг " + getArch(missions[0]['archwingRequired']), inline=True)
    embed.add_field(name=missions[1]["type"], value=missions[1]["node"] + "\n\nАрчвинг " + getArch(missions[1]['archwingRequired']), inline=True)
    embed.add_field(name=missions[2]["type"], value=missions[2]["node"] + "\n\nАрчвинг " + getArch(missions[2]['archwingRequired']), inline=True)
    embed.add_field(name="Босс", value=response["boss"])
    embed.add_field(name="До конца охоты", value=response["eta"])

    await ctx.send(embed=embed)

@bot.command()
async def constr(ctx):
    response = getResponse(5)
    embed = discord.Embed(
        title="Прогресс постройки",
        color=0x0000FF
    )
    embed.add_field(name="Фоморианец", value=response["fomorianProgress"] + "%", inline=True)
    embed.add_field(name="Армада секачей", value=response["razorbackProgress"] + "%", inline=True)

    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Команды бота",
        color=0x0000FF
    )
    embed.add_field(name=".cetus", value="Узнать время суток на Цетусе", inline=False)
    embed.add_field(name=".earth", value="Узнать время суток на Земле (обычные миссии)", inline=False)
    embed.add_field(name=".camb", value="Цикл Камбионийского дрейфа. Фэз или Воум", inline=False)
    embed.add_field(name=".arbi", value="Данные арбитража", inline=False)
    embed.add_field(name=".hunt", value="Охота на Архонта", inline=False)
    embed.add_field(name=".constr", value="Прогресс постройки Фоморианца и Армады секачей", inline=False)

    await ctx.send(embed=embed)

bot.run(settings["token"])