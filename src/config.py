import os
import json
from dotenv import load_dotenv

with open(os.path.join(os.path.dirname(__file__), '../config.json'), "r") as file:
	CONFIG = json.load(file)

load_dotenv()

class config:
	PREFIX = os.getenv("PREFIX") or CONFIG["PREFIX"]
	
	class SHARED:
		deletionQueueSize = os.getenv("SHARED_DELETION_QUEUE_SIZE") or CONFIG["SHARED"]["deletionQueueSize"]
		
	class SHOUTBOX:
		channel = os.getenv("SHOUTBOX_CHANNEL") or CONFIG["SHOUTBOX"]["channel"]
		
	class REQUESTS:
		class retry:
			total = os.getenv("REQUESTS_RETRY_TOTAL") or CONFIG["REQUESTS"]["retry"]["total"]
			status_forcelist = os.getenv("REQUESTS_RETRY_STATUS_FORCELIST") or CONFIG["REQUESTS"]["retry"]["status_forcelist"]
			method_whitelist = os.getenv("REQUESTS_RETRY_METHOD_WHITELIST") or CONFIG["REQUESTS"]["retry"]["method_whitelist"]
			
	class TIPLANET:
		host = os.getenv("TIPLANET_HOST") or CONFIG["TIPLANET"]["host"]
		login = os.getenv("TIPLANET_LOGIN") or CONFIG["TIPLANET"]["login"]
		logout = os.getenv("TIPLANET_LOGOUT") or CONFIG["TIPLANET"]["logout"]
		
		class cookies:
			sid = os.getenv("TIPLANET_COOKIES_SID") or CONFIG["TIPLANET"]["cookies"]["sid"]
			
		chat = os.getenv("TIPLANET_CHAT") or CONFIG["TIPLANET"]["chat"]
		keepAwake = os.getenv("TIPLANET_KEEPAWAKE") or CONFIG["TIPLANET"]["keepAwake"]
		pollingInterval = os.getenv("TIPLANET_POLLINGINTERVAL") or CONFIG["TIPLANET"]["pollingInterval"]
		
		class user:
			username = os.getenv("TIPLANET_USER_USERNAME")
			password = os.getenv("TIPLANET_USER_PASSWORD")
			
		selfBot = os.getenv("TIPLANET_SELFBOT") or CONFIG["TIPLANET"]["selfBot"]
		
		class webhook:
			id = os.getenv("TIPLANET_WEBHOOK_ID")
			token = os.getenv("TIPLANET_WEBHOOK_TOKEN")
		
		class thumbnails:
			maxWidth = os.getenv("TIPLANET_THUMBNAILS_MAXWIDTH") or CONFIG["TIPLANET"]["thumbnails"]["maxWidth"]
			maxHeight = os.getenv("TIPLANET_THUMBNAILS_MAXHEIGHT") or CONFIG["TIPLANET"]["thumbnails"]["maxHeight"]
			
		emojis = {
			":troll:": "<:troll:810143192581668885:>",
			":wat:": "<:wat:810143891855507517:>",
            ":p": ":stuck_out_tongue:"
		}
		censure = {
			"merde": "saperlipopette",
			"bordel": "sapristi",
			"foutre": "faire",
			"chiant": "très embettant",
			"couille": "bonbon",
			"putain": "fichtre",
			"putin": "fichtre",
			"prenium": "premium",
			"pretium": "premium",
			"bonjours": "bonjour",
			"ce jeux": "ce jeu",
			"le jeux": "le jeu",
			"un jeux": "un jeu",
			"du jeux": "du jeu",
			"enfaite": "en fait"
		}	
		class irc:
			id = os.getenv("TIPLANET_IRC") or CONFIG["TIPLANET"]["irc"]["id"]
		
	class DISCORD:
		token = os.getenv('DISCORD_TOKEN')
		class cogs:
			class latex:
				enable = os.getenv("DISCORD_LATEX_ENABLE") or CONFIG["DISCORD"]["cogs"]["latex"]["enable"]
