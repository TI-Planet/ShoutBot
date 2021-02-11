#!/usr/bin/env python3

import json

from discord.ext import commands

from src.tiplanet import tiplanet

def action() :
	print("test")

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


bot.run(config["TOKEN"])
