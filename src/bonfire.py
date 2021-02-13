class bonfire:
	def __init__(self, config, bot, chat):
		self.config = config
		self.chat = chat
		self.bot = bot
	

	def updateChat(self, message):
		if message.author == self.bot.user or str(message.webhook_id) == str(self.config["TIPLANET"]["webhook"]["id"]):
			return

		if (message.channel.id == self.config["SHOUTBOX"]["channel"]):
			self.chat.postChatMessage(self.generateMessage(message))


	def generateMessage(self, message):
		if (message.reference):
			ref = message.reference
			return f"[b]{self.removeDiscordID(message.author)}[/b] : [quote={self.removeDiscordID(ref.resolved.author)}]{ref.resolved.content}[/quote] {message.content}"
		else : 
			return f"[b]{self.removeDiscordID(message.author)}[/b] : {message.content}"


	def removeDiscordID(self, username):
		return str(username)[0:-5]
