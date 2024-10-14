import discord
from discord.ext import commands
import requests

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='qr')
async def generate_qr(ctx, *, text):
    qr_api_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={text}"
    
    response = requests.get(qr_api_url)
    if response.status_code == 200:
        with open("qr_code.png", "wb") as file:
            file.write(response.content)
        
        await ctx.send(file=discord.File("qr_code.png"))
    else:
        await ctx.send("Failed to generate QR code. Please try again.")

@bot.command(name='shorten')
async def shorten_link(ctx, *, url):
    api_url = "https://is.gd/create.php"
    params = {
        "format": "simple",
        "url": url
    }
    
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        await ctx.send(f"Shortened URL: {response.text}")
    else:
        await ctx.send("Failed to shorten the URL. Please try again.")

@bot.command(name='fact')
async def random_fact(ctx):
    response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
    if response.status_code == 200:
        fact = response.json().get("text")
        await ctx.send(f"Did you know? {fact}")
    else:
        await ctx.send("Couldn't fetch a fact at the moment. Try again later.")

@bot.command(name='joke')
async def random_joke(ctx):
    response = requests.get("https://official-joke-api.appspot.com/random_joke")
    if response.status_code == 200:
        joke = response.json()
        await ctx.send(f"{joke['setup']} - {joke['punchline']}")
    else:
        await ctx.send("Couldn't fetch a joke at the moment. Try again later.")

import discord
from discord.ext import commands

@bot.command(name='helpme')
async def custom_help(ctx):
    embed = discord.Embed(
        title="Help Menu",
        description="**Here are the commands you can use:**",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="`!qr <text>`",
        value="Generate a QR code for the given text.",
        inline=False
    )
    embed.add_field(
        name="`!shorten <url>`",
        value="Shorten a URL using a link shortener.",
        inline=False
    )
    embed.add_field(
        name="`!fact`",
        value="Get a random interesting fact.",
        inline=False
    )
    embed.add_field(
        name="`!joke`",
        value="Hear a random joke.",
        inline=False
    )
    embed.add_field(
        name="`!helpme`",
        value="Show this help message.",
        inline=False
    )
    
    embed.set_footer(text="Made with <3 by @M0HID")
    
    await ctx.send(embed=embed)


bot.run(SECRET_BOT_TOKEN)
