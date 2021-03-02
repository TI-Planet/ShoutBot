from .parser import Parser

class bonfire:
	def __init__(self, config, bot, chat, cogs):
		self.config = config
		self.chat = chat
		self.bot = bot
		self.parser = Parser(self.config)
		self.commands = cogs.getCommands()

	def updateChat(self, message):
		if message.author == self.bot.user or str(message.webhook_id) == str(self.config.TIPLANET.webhook.id):
			return

		if message.content in self.commands:
			return

		if (message.channel.id == self.config.SHOUTBOX.channel):
			try:
				chat_id = self.chat.postChatMessage(self.generateMessage(message))
			except:
				raise("error while updating chat")

			if chat_id != None:
				self.chat.deletionQueue[self.chat.deletionQueueIndex] = (int(chat_id), message.id)
				self.chat.deletionQueueIndex = (self.chat.deletionQueueIndex + 1) % len(self.chat.deletionQueue)


	def generateMessage(self, message):
		quotePrefix = ''
		attachmentSuffix = ''

		# this is a reply, add quote
		if (message.reference):
			ref = message.reference
			quote = ref.resolved.clean_content
			quote = self.parser.remove_quotes(quote)
			quote = self.parser.parse_markdown2bbcode(quote)
			quotePrefix = f'[quote={self.removeDiscordID(ref.resolved.author)}]{quote}[/quote] '

		# this contains files
		if (message.attachments != None and len(message.attachments) != 0):
			attachmentSuffix = '\n'.join([self.attachmentToString(a) for a in message.attachments])
			attachmentSuffix = f'\n{attachmentSuffix}'

		name = f"[b][color=block]{'[IRC] ' if str(message.webhook_id) == str(self.config.TIPLANET.irc.id) else ''}{self.removeDiscordID(message.author)}[/color][/b]: "

		msg = self.parser.parse_markdown2bbcode(message.clean_content)

		return f"{f'{self.config.DEVPREFIX}{name}' if not self.config.TIPLANET.selfBot else ''}{quotePrefix}{msg}{attachmentSuffix}"

	def removeDiscordID(self, username):
		return str(username)[0:-5]

	def attachmentToString(self, attachment):
		extension = attachment.url.split('.')[-1]

		if attachment.width != None and extension in ['png', 'jpg', 'jpeg', 'gif', 'bmp']:
			width, height = self.thumbnailDimensions(attachment.width, attachment.height)
			ret = f'[url={attachment.url}][img]{attachment.proxy_url}?width={width}&height={height}[/img][/url]'
		else:
			basename = attachment.url.split('/')[-1]
			ret = f'[url={attachment.url}]{basename}[/url]'

		if attachment.is_spoiler():
			ret = f'[ispoiler]{ret}[/ispoiler]'

		return ret

	def thumbnailDimensions(self, width, height):
		max_w = self.config.TIPLANET.thumbnails.maxWidth
		max_h = self.config.TIPLANET.thumbnails.maxHeight
		computed_w = width * max_h/height
		computed_h = height * max_w/width
		if max_w * computed_h < computed_w * max_h:
			return (int(max_w), int(computed_h))
		else:
			return (int(computed_w), int(max_h))

	def deleteChat(self, message):
		if message.author == self.bot.user:
			return
		if (message.channel.id == self.config.SHOUTBOX.channel):
			try:
				id = message.id
				candidates = [tp_id for tp_id, ds_id in self.chat.deletionQueue if ds_id == int(id)]
				if len(candidates) == 0:
					return
				tp_id = candidates[0]
				self.chat.deleteChatMessage(tp_id)
			finally:
				pass
