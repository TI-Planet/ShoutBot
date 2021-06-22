import os
import re
import urllib

import requests

from discord import File
from discord.ext import commands


class Latex(commands.Cog):
	def __init__(self, bot, config):
		self.bot = bot
		self.config = config.DISCORD.cogs.latex

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author == self.bot.user:
			return

		os.makedirs("latex", exist_ok=True)
		latexMsgs = re.findall(r"\$\$([\s\S]*?)\$\$", message.content)

		if latexMsgs:
			ctx = await self.bot.get_context(message)
			await message.add_reaction("🔍")
			latexImg = []
			latexFiles = []
			async with ctx.typing():
				try:
					for i in range(len(latexMsgs)):
						img = requests.get(f"https://chart.googleapis.com/chart?cht=tx&chco=FFFFFF&chf=bg,s,36393F&chl={urllib.parse.quote(latexMsgs[i])}", stream=True)
						if img.status_code == 200:
							with open(os.path.join(os.path.dirname(__file__), f"../../latex/{message.id}-{i}.png"), 'wb') as file:
								for chunk in img:
									file.write(chunk)
								latexImg.append(f"../../latex/{message.id}-{i}.png")

					for file in latexImg:
						with open(os.path.join(os.path.dirname(__file__), file), 'rb') as image:
							latexFiles.append(File(image))

					await message.reply(files=latexFiles, mention_author=False)
					await message.clear_reaction("🔍")
					await message.add_reaction("✅")
				except:
					await message.add_reaction("❌")

			for file in latexImg:
				os.remove(os.path.join(os.path.dirname(__file__), file))
