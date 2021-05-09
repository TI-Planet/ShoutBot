import os
import json

with open(os.path.join(os.path.dirname(__file__), '../config.json'), "r", encoding='utf-8') as file:
	config_default = json.load(file)
with open(os.path.join(os.path.dirname(__file__), '../config_override.json'), "r", encoding='utf-8') as file:
	config_override = json.load(file)

def config_field(names, defaultValue=None):
	global config_default, config_override
	def load(cfg):
		ret = cfg
		for name in names:
			if not name in ret:
				return None
			ret = ret[name]
		return ret
	for v in [load(config_override), load(config_default)]:
		if v != None: return v
	return defaultValue

class config:
	PREFIX = config_field(["PREFIX"])
	DEVPREFIX = config_field(["DEVPREFIX"]) or ""

	class SHARED:
		deletionQueueSize = config_field(["SHARED", "deletionQueueSize"])

	class SHOUTBOX:
		channel = config_field(["SHOUTBOX", "channel"])

	class REQUESTS:
		class retry:
			total = config_field(["REQUESTS", "retry", "total"])
			status_forcelist = config_field(["REQUESTS", "retry", "status_forcelist"])
			method_whitelist = config_field(["REQUESTS", "retry", "method_whitelist"])

	class TIPLANET:
		localServer = config_field(["TIPLANET", "localServer"], defaultValue=False)
		host = config_field(["TIPLANET", "host"])
		login = config_field(["TIPLANET", "login"])
		logout = config_field(["TIPLANET", "logout"])
		TiBotId = int(config_field(["TIPLANET", "TiBotId"]))

		class cookies:
			sid = config_field(["TIPLANET", "cookies", "sid"])

		chat = config_field(["TIPLANET", "chat"])
		keepAwake = config_field(["TIPLANET", "keepAwake"])
		pollingInterval = config_field(["TIPLANET", "pollingInterval"])

		class user:
			username = config_field(["TIPLANET", "USER", "USERNAME"])
			password = config_field(["TIPLANET", "USER", "PASSWORD"])

		bots = config_field(["TIPLANET", "bots"])

		selfBot = config_field(["TIPLANET", "selfBot"])

		sendConnections = config_field(["TIPLANET", "sendConnections"])

		class webhook:
			id = config_field(["TIPLANET", "WEBHOOK", "ID"])
			token = config_field(["TIPLANET", "WEBHOOK", "TOKEN"])

		class thumbnails:
			maxWidth = config_field(["TIPLANET", "thumbnails", "maxWidth"])
			maxHeight = config_field(["TIPLANET", "thumbnails", "maxHeight"])

		roles = config_field(["TIPLANET", "roles"])
		emojis = config_field(["TIPLANET", "emojis"])
		censorship = config_field(["TIPLANET", "censorship"])
		notif = config_field(["TIPLANET", "notif"])

		class irc:
			id = config_field(["TIPLANET", "irc", "id"])

	class DISCORD:
		token = config_field(["DISCORD", "TOKEN"])
		useDisplayName = config_field(["DISCORD", "useDisplayName"])
		roles = config_field(["DISCORD", "roles"])
		class cogs:
			class latex:
				enable = config_field(["DISCORD", "cogs", "latex", "enable"])
