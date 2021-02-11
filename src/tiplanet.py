import requests

from bs4 import BeautifulSoup


class tiplanet:
	def __init__(self, config):
		self.config = config["TIPLANET"]
		self.session = requests.Session()
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

		payload = {
			'username': self.config["user"]["username"],
			'password': self.config["user"]["password"],
		}

		self.session.post(logoutUrl, data=payload)

	def getChat(self):
		r = self.session.get(self.getUrl(self.config["chat"]))
		print(r.text)

	def getUrl(self, url):
		return f"https://{self.config['host']}{url}"
