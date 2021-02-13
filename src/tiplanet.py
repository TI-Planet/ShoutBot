import json
import requests
from bs4 import BeautifulSoup
from discord import Webhook, RequestsWebhookAdapter, AllowedMentions

from .bbcodeParser import bbcodeParser


class tiplanet:
	def __init__(self, config):
		self.config = config["TIPLANET"]
		self.session = requests.Session()
		self.parser = bbcodeParser()
		self.webhook = Webhook.partial(self.config['webhook']['id'], self.config['webhook']['token'], adapter=RequestsWebhookAdapter())
		self.lastId = None
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

		messages = [message for message in messages if not message["content"].startswith("/log") ]

		return messages

	def updateChat(self):
		messages = self.getChat()

		if self.lastId == None:
			self.lastId = messages[-1]["id"]

		for message in messages:
			if int(message["id"]) > int(self.lastId) and message["userName"] != self.config["user"]["username"]:
				self.postDiscordMessage(message)

		self.lastId = messages[-1]["id"]


	def postDiscordMessage(self, message):
		self.webhook.send(
			message["content"],
			avatar_url=f"https://tiplanet.org/forum/avatar.php?id={message['userId']}",
			username=message["userName"],
			allowed_mentions=AllowedMentions(everyone=False, users=False, roles=False, replied_user=False)
		)


	def postChatMessage(self, message, channel="Public"):
		payload = {
			"channelName": channel,
			"text": message
		}
		self.session.post(self.getUrl(self.config["chat"]), data=payload)

	def getUrl(self, url):
		return f"https://{self.config['host']}{url}"

