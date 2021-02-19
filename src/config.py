import os
import json

with open(os.path.join(os.path.dirname(__file__), '../config.json'), "r") as file:
	config_default = json.load(file)
with open(os.path.join(os.path.dirname(__file__), '../config_override.json'), "r") as file:
	config_override = json.load(file)

def config_field(names):
	global config_default, config_override
	def load(cfg):
		ret = cfg
		for name in names:
			if not name in ret:
				return None
			ret = ret[name]
		return ret
	return load(config_override) or load(config_default)

class config:
	PREFIX = config_field(["PREFIX"])

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
		host = config_field(["TIPLANET", "host"])
		login = config_field(["TIPLANET", "login"])
		logout = config_field(["TIPLANET", "logout"])

		class cookies:
			sid = config_field(["TIPLANET", "cookies", "sid"])

		chat = config_field(["TIPLANET", "chat"])
		keepAwake = config_field(["TIPLANET", "keepAwake"])
		pollingInterval = config_field(["TIPLANET", "pollingInterval"])

		class user:
			username = config_field(["TIPLANET", "USER", "USERNAME"])
			password = config_field(["TIPLANET", "USER", "PASSWORD"])

		selfBot = config_field(["TIPLANET", "selfBot"])

		class webhook:
			id = config_field(["TIPLANET", "WEBHOOK", "ID"])
			token = config_field(["TIPLANET", "WEBHOOK", "TOKEN"])

		class thumbnails:
			maxWidth = config_field(["TIPLANET", "thumbnails", "maxWidth"])
			maxHeight = config_field(["TIPLANET", "thumbnails", "maxHeight"])

		emojis = config_field(["TIPLANET", "emojis"])

		class irc:
			id = config_field(["TIPLANET", "irc", "id"])

	class DISCORD:
		token = config_field(["DISCORD", "TOKEN"])
		class cogs:
			class latex:
				enable = config_field(["DISCORD", "cogs", "latex", "enable"])
