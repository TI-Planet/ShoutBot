#!/usr/bin/env python3

import time
import asyncio
from discord.ext import commands

from src.config import config
from src.bonfire import bonfire
from src.tiplanet import tiplanet


__version__ = "under developpement"

config = config().LoadConfig()
bot = commands.Bot(command_prefix=config["PREFIX"])
chat = tiplanet(config)
discord = bonfire(config, bot, chat)


@bot.event
async def on_ready():
	print(f"Bot {bot.user.name} connected on {len(bot.guilds)} servers")
	while True:
		chat.updateChat()
		await asyncio.sleep(2)


@bot.event
async def on_message(message):
	discord.updateChat(message)


try:
	bot.run(config["DISCORD_TOKEN"])
finally:
	print('EXITING GRACEFULLY')
