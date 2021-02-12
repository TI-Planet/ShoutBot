import os
import json
from dotenv import load_dotenv


class config:
    def __init__(self) -> None:
        self.config = None
        pass


    def LoadConfig(self):
        self.loadConfigFile()
        self.loadEnv()
        return self.config
        


    def loadConfigFile(self):
        with open(os.path.join(os.path.dirname(__file__), '../config.json'), "r") as file:
	        self.config = json.load(file)


    def loadEnv(self):
        load_dotenv()
        self.config["DISCORD_TOKEN"] = os.getenv('DISCORD_TOKEN')
        self.config["TIPLANET"]["user"]["username"] = os.getenv('TIPLANET_USER_USERNAME') 
        self.config["TIPLANET"]["user"]["password"] = os.getenv('TIPLANET_USER_PASSWORD') 
        self.config["TIPLANET"]['webhook']['id'] = os.getenv('TIPLANET_WEBHOOK_ID') 
        self.config["TIPLANET"]['webhook']['token'] = os.getenv('TIPLANET_WEBHOOK_TOKEN') 
