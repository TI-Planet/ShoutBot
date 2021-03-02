from discord.ext import commands
import discord
import os

class admin(commands.Cog):
	def __init__(self, bot, config):
		self.config = config.DISCORD
		self.bot = bot
	@commands.command(name="pull")
	async def pull(self, ctx):
		if ctx.author.id not in self.config.owners:
			return
		try: await ctx.message.delete()
		except: pass
		done = os.system("git pull")
		if done == 0:
			await ctx.send("✅ Le repo github a été correctement pull.", delete_after=5)
		else:
			await ctx.send("❌ Une erreur est survenue lors du pull.", delete_after=5)