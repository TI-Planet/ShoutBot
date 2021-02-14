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
		quotePrefix = ''
		attachmentSuffix = ''

		# this is a reply, add quote
		if (message.reference):
			ref = message.reference
			quotePrefix = f'[quote={self.removeDiscordID(ref.resolved.author)}]{ref.resolved.content}[/quote] '

		# this contains files
		if (message.attachments != None and len(message.attachments) != 0):
			attachmentSuffix = '\n'.join([attachmentToString(a) for a in message.attachments])
			attachmentSuffix = f'\n{attachmentSuffix}'

		return f"[b]{self.removeDiscordID(message.author)}[/b] : {quotePrefix}{message.content}{attachmentSuffix}"

	def removeDiscordID(self, username):
		return str(username)[0:-5]

def attachmentToString(attachment):
	extension = attachment.url.split('.')[-1]

	if attachment.width != None and extension in ['png', 'jpg', 'jpeg', 'gif', 'bmp']:
		width, height = thumbnailDimensions(attachment.width, attachment.height)
		ret = f'[url={attachment.url}][img]{attachment.proxy_url}?width={width}&height={height}[/img][/url]'
	else:
		basename = attachment.url.split('/')[-1]
		ret = f'[url={attachment.url}]{basename}[/url]'

	if attachment.is_spoiler():
		ret = f'[ispoiler]{ret}[/ispoiler]'

	return ret

def thumbnailDimensions(width, height):
	# TODO
	# - use config rather than hardcode values
	# - keep proportions
	return (50, 50)
