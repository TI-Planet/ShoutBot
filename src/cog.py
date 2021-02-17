from .cogs.latex import Latex

class Cog:
    def __init__(self, config, bot):
        self.config = config
        self.cogs = config.DISCORD.cogs
        self.bot = bot
    
    def LoadCogs(self):
        if self.cogs.latex.enable:
            self.bot.add_cog(Latex(self.bot, self.config))
