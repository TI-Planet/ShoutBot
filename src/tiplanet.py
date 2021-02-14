import json
import requests
from bs4 import BeautifulSoup
from discord import Webhook, RequestsWebhookAdapter, AllowedMentions, Object

from .bbcodeParser import bbcodeParser


class tiplanet:
	def __init__(self, config):
		self.channel = config["SHOUTBOX"]["channel"]
		self.config = config["TIPLANET"]
		self.session = requests.Session()
		self.parser = bbcodeParser(self.config)
		self.webhook = Webhook.partial(self.config['webhook']['id'], self.config['webhook']['token'], adapter=RequestsWebhookAdapter())
		self.lastId = None
		self.deletionQueue = [(0, 0) for i in range(config["SHARED"]["deletionQueueSize"])]
		self.deletionQueueIndex = 0
		self.login()

	def login(self):
		loginUrl = self.getUrl(self.config["login"])

		payload = {
			'username': self.config["user"]["username"],
			'password': self.config["user"]["password"],
			'autologin': 'true',
			'viewonline': 'false',
			'redirect': '',
			'login': 'Connexion'
		}

		self.session.post(loginUrl, data=payload)

	def logout(self):
		logoutUrl = self.getUrl(self.config["logout"])
		sid = self.session.cookies.get_dict()[self.config["cookies"]["sid"]]

		payload = {
			'username': self.config["user"]["username"],
			'password': self.config["user"]["password"],
		}

		self.session.post(f"{logoutUrl}&sid={sid}", data=payload)

	def getChat(self):
		chat = self.session.get(self.getUrl(self.config["chat"]))
		soup = BeautifulSoup(chat.text, "html.parser")

		messages = [{
			"id": message.get("id"),
			"userId": message.get("userid"),
			"userRole": message.get("userrole"),
			"userName": message.username.text,
			"content": self.parser.parse_bbcode2markdown(message.find('text').text)
		} for message in soup.find_all("message")]

		return messages

	async def updateChat(self, bot):
		messages = self.getChat()
		lastId = messages[-1]["id"]

		if self.lastId == None:
			self.lastId = lastId

		# keep recent content only
		messages = [m for m in messages if int(m["id"]) > int(self.lastId) and m["userName"] != self.config["user"]["username"]]

		self.lastId = lastId

		# split between deletions and actual messages
		deletions = [m for m in messages if m['content'].startswith('/delete')]
		messages = [m for m in messages if not m['content'].startswith('/delete')]

		for deletion in deletions:
			await self.deleteDiscordMessage(bot, deletion['content'].strip().split(' ')[-1])

		for message in messages:
			self.postDiscordMessage(message)

	async def deleteDiscordMessage(self, bot, id):
		try:
			candidates = [ds_id for tp_id, ds_id in self.deletionQueue if tp_id == int(id)]
			if len(candidates) == 0:
				return
			ds_id = candidates[0]
			channel = await bot.fetch_channel(self.channel)
			await channel.delete_messages([Object(ds_id)])
		finally:
			pass

	def postDiscordMessage(self, message):
		if message["content"].startswith("/log"):
			return

		ds_msg = self.webhook.send(
			message["content"],
			wait=True, # so we can get the ds_msg
			avatar_url=f"https://tiplanet.org/forum/avatar.php?id={message['userId']}",
			username=message["userName"],
			allowed_mentions=AllowedMentions(everyone=False, users=False, roles=False, replied_user=False)
		)
		if ds_msg != None:
			self.deletionQueue[self.deletionQueueIndex] = (int(message["id"]), ds_msg.id)
			self.deletionQueueIndex = (self.deletionQueueIndex + 1) % len(self.deletionQueue)


	def postChatMessage(self, message, channel="Public"):
		payload = {
			"channelName": channel,
			"text": message
		}
		self.session.post(self.getUrl(self.config["chat"]), data=payload)

	def getUrl(self, url):
		return f"https://{self.config['host']}{url}"

