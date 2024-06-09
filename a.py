import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus der token.env-Datei
load_dotenv(dotenv_path='token.env')

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
CHANNEL_ID = '1249474499343159326'

bot = commands.Bot(command_prefix='!')

# Definieren des absoluten Pfads zur Liste
LIST_PATH = r'C:\Users\adaro\Desktop\RECHNUNGEN BOT DISCORD\Liste.txt'

@bot.event
async def on_ready():
    print(f'{bot.user} ist bereit!')
    channel = bot.get_channel(int(CHANNEL_ID))  # Konvertiere CHANNEL_ID in eine Ganzzahl
    await clear_messages(channel)
    await show_commands(channel)

async def clear_messages(channel):
    async for message in channel.history(limit=100):
        await message.delete()

async def show_commands(channel):
    embed = discord.Embed(title="Rechnungs bot", color=0x00ff00)
    embed.add_field(name="Befehle:", value="!add (Name) (Zu Zahlen) (Email) (Zahlungsdatum)\n!remove (Name)", inline=False)
    embed.set_footer(text="made by cxdery")

    message = await channel.send(embed=embed)
    print("Befehle gesendet")

@bot.command(name='add')
async def add(ctx, *, args):
    with open(LIST_PATH, 'a') as f:
        f.write(args + '\n')
    
    print(f"Neue Rechnung hinzugefügt: {args}")
    await refresh_list(ctx)

@bot.command(name='remove')
async def remove(ctx, *, name):
    lines = []
    with open(LIST_PATH, 'r') as f:
        lines = f.readlines()

    with open(LIST_PATH, 'w') as f:
        for line in lines:
            if name not in line.split()[0]:
                f.write(line)
    
    print(f"Rechnung entfernt: {name}")
    await refresh_list(ctx)

@bot.command(name='Rechnung')
async def show_list(ctx):
    await refresh_list(ctx)

async def refresh_list(ctx):
    with open(LIST_PATH, 'r') as f:
        content = f.read()

    embed = discord.Embed(title="Rechnungen", color=0x00ff00)
    if content.strip() == "":
        embed.add_field(name="Liste:", value="Leer", inline=False)
    else:
        embed.add_field(name="Liste:", value=content, inline=False)
    embed.add_field(name="Befehle:", value="!add (Name) (Zu Zahlen) (Email) (Zahlungsdatum)\n!remove (Name)", inline=False)
    embed.set_footer(text="")

    if ctx.message:
        await ctx.message.delete()

    async for message in ctx.channel.history(limit=1):
        await message.delete()

    message = await ctx.send(content="@everyone", embed=embed)
    await message.add_reaction('')
    print("")

@bot.event
async def on_reaction_add(reaction, user):
    if user != bot.user and reaction.emoji == '':
        await reaction.message.delete()

if TOKEN is None:
    raise ValueError("Das Discord-Token wurde nicht geladen. Stelle sicher, dass die token.env-Datei korrekt ist.")

bot.run(TOKEN)
