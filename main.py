#!/usr/bin/env python3

import time
import asyncio
from discord.ext import commands

from src.config import config
from src.tiplanet import tiplanet


__version__ = "under developpement"

config = config().LoadConfig()
bot = commands.Bot(command_prefix=config["PREFIX"])
chat = tiplanet(config)


@bot.event
async def on_ready():
	print(f"Bot {bot.user.name} connected on {len(bot.guilds)} servers")
	while True:
		chat.updateChat()
		await asyncio.sleep(2)

@bot.event
async def on_message(message):
	if message.author == bot.user:
		return

	# if (message.channel.id == config["SHOUTBOX"]["channel"]):
	# 	await message.channel.send(message.content)

try:
	bot.run(config["DISCORD_TOKEN"])
finally:
	print('EXITING GRACEFULLY')
