#!/usr/bin/env python3

import asyncio
import time

import discord
from discord.ext import commands

from src.bonfire import bonfire
from src.cog import Cog
from src.config import config
from src.tiplanet import tiplanet


__version__ = "under developpement"

bot = commands.Bot(command_prefix=config.PREFIX)
chat = tiplanet(config)
cogs = Cog(config, bot, chat)
discord = bonfire(config, bot, chat, cogs)


@bot.event
async def on_ready():
	print(f"Bot {bot.user.name} connected on {len(bot.guilds)} server{'s'*(len(bot.guilds)>1)}")
	while True:
		try:
			await chat.updateChat(bot)
		except:
			pass
		await asyncio.sleep(config.TIPLANET.pollingInterval)


@bot.event
async def on_message(message):
	await discord.updateChat(message)
	await bot.process_commands(message)


@bot.event
async def on_message_delete(message):
	discord.deleteChat(message)


try:
	bot.run(config.DISCORD.token)
finally:
	chat.logout()
	print('EXITING GRACEFULLY')
