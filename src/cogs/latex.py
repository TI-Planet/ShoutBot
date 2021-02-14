import os
import re
from discord import File
from pnglatex import pnglatex
from discord.ext import commands


class Latex(commands.Cog):
	def __init__(self, bot, config):
		self.bot = bot
		self.config = config["DISCORD"]["cogs"]["latex"]

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author == self.bot.user:
			return

		os.makedirs("latex", exist_ok=True)
		latexMsgs = re.findall(r"\$\$(.*?)\$\$", message.content)
		latexImages = []
		latexFiles = []
		if (latexMsgs):
			ctx = await self.bot.get_context(message)
			await message.add_reaction("🔍")
			async with ctx.typing():
				for i in range(len(latexMsgs)):
					try:
						latexImages.append(pnglatex(f"\[\displaystyle{{{latexMsgs[i]}}}\]", f"latex/{message.id}-{i}.png"))
					except:
						await message.add_reaction("❌")
				for file in latexImages:
					with open(file, 'rb') as image:
						latexFiles.append(File(image))
				await message.reply(files=latexFiles, mention_author=False)
				await message.clear_reaction("🔍")
				await message.add_reaction("✅")
			for file in latexImages:
				os.remove(file)
			




		
