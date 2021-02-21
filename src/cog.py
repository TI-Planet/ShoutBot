from .cogs.latex import Latex
from .cogs.chat import Chat

class Cog:
	def __init__(self, config, bot, chat):
		self.cogs = config.DISCORD.cogs
		self.config = config
		self.chat = chat
		self.bot = bot
		self.commands = []

		self.LoadCogs()
	
	def LoadCogs(self):
		if self.cogs.latex.enable:
			self.bot.add_cog(Latex(self.bot, self.config))
			self.registerCommands(self.bot.get_cog('Latex'))
		
		self.bot.add_cog(Chat(self.bot, self.config, self.chat))
		self.registerCommands(self.bot.get_cog('Chat'))

	def registerCommands(self, cog):
		for c in cog.get_commands():
			self.commands.append(f"{self.config.PREFIX}{c.name}")

	def getCommands(self):
		return self.commands

