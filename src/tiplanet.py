import json
import requests
from bs4 import BeautifulSoup

from .bbcodeParser import bbcodeParser


class tiplanet:
	def __init__(self, config):
		self.config = config["TIPLANET"]
		self.session = requests.Session()
		self.parser = bbcodeParser()
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

		messages = []

		for message in soup.find_all("message"):
			messages.append({
				"id": message.get("id"),
				"userId": message.get("userid"),
				"userRole": message.get("userrole"),
				"userName": message.username.text,
				"content": self.parser.parse_bbcode2markdown(message.find('text').text)
			})

		for message in messages:
			self.postMessage(message)
		return messages

	def postMessage(self, message):
		payload = {
			"username": message["userName"],
			"avatar_url": f"https://tiplanet.org/forum/avatar.php?id={message['userId']}",
			"content": message["content"],
			"allowed_mentions": {
				"parse": []
			}
		}
		requests.post(f"https://discord.com/api/webhooks/{self.config['webhook']['id']}/{self.config['webhook']['token']}", headers={'Content-Type': 'application/json'}, data=json.dumps(payload))

	def getUrl(self, url):
		return f"https://{self.config['host']}{url}"

