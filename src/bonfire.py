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

			if chat_id != None and not message.content.startswith('/'):
				self.chat.deletionQueue[self.chat.deletionQueueIndex] = (int(chat_id), message.id)
				self.chat.deletionQueueIndex = (self.chat.deletionQueueIndex + 1) % len(self.chat.deletionQueue)
				self.chat.connectionMsg = None


	def generateMessage(self, message):
		quotePrefix = ''
		attachmentSuffix = ''

		# this is a reply, add quote and potential /msg
		if (message.reference):
			ref = message.reference
			author = self.getName(ref.resolved.author)

			quote = ref.resolved.clean_content
			quote = self.parser.remove_quotes(quote)
			quote = self.parser.parse_markdown2bbcode(quote)

			privPrefix = ''
			if ' (murmure)' in author:
				privPrefix = f'/msg {author.split(" (murmure)")[0]} '
				author = author.replace(' (murmure)', '')

			quotePrefix = f'{privPrefix}[quote={author}]{quote}[/quote] '

		# this contains files
		if (message.attachments != None and len(message.attachments) != 0):
			attachmentSuffix = '\n'.join([self.attachmentToString(a) for a in message.attachments])
			attachmentSuffix = f'\n{attachmentSuffix}'

		name = f"{self.config.DEVPREFIX}{self.getName(message.author)}"
		name = f"{name}{' ☎️' if str(message.webhook_id) == str(self.config.TIPLANET.irc.id) else ''}"
		name = f"[url={str(message.author.avatar_url).split('cdn.discordapp.com/')[-1]}]{name}[/url]"
		name = f"[b][color={self.getColor(message.author)}]{name}[/color][/b]: "

		msg = self.parser.parse_markdown2bbcode(message.clean_content)

		return f"{name if not self.config.TIPLANET.selfBot else ''}{quotePrefix}{msg}{attachmentSuffix}"

	def getColor(self, author):
		try:
			roleIds = [int(role.id) for role in author.roles]
			for roleId, value in self.config.DISCORD.roles.items():
				if int(roleId) in roleIds:
					return value.split('//')[0].strip()
		except:
			pass
		return 'block'

	def getName(self, user):
		return user.display_name if self.config.DISCORD.useDisplayName else user.name

	def attachmentToString(self, attachment):
		extension = attachment.url.split('.')[-1].lower()

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
