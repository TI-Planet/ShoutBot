#!/usr/bin/env python3

import os
import json
from dotenv import load_dotenv
from discord.ext import commands

from src.tiplanet import tiplanet

load_dotenv()

__version__ = "under developpement"

# Configuration
with open("config.json", "r") as file:
	config = json.load(file)


bot = commands.Bot(command_prefix=config["PREFIX"])
chat = tiplanet(config)


@bot.event
async def on_ready():
	print(f"Bot {bot.user.name} connected on {len(bot.guilds)} servers")


@bot.event
async def on_message(message):
	if message.author == bot.user:
		return

	if (message.channel.id == config["SHOUTBOX"]["channel"]):
		await message.channel.send(message.content)


bot.run(os.getenv('DISCORD_TOKEN'))
