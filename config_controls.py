from exceptions import ConfigError
import json
import os

class ConfigControls:
	def __init__(self):
		self.target = "config.json"
		self.current_config = {}
		self.template_config = {
			"bot_token":"",
			"server_script":"",
			"server_args":[],
			"default_server_guild":0,
			"default_server_channel":0,
			"default_admins":[]
		}
		if not os.path.isfile(self.target):
			with open(self.target, "w+") as f:
				json.dump(self.template_config,f,indent=4)
	def read_configs(self):
		if not os.path.isfile(self.target):
			raise ConfigError(f"Config file at {self.target} not found.")
		with open(self.target, "r") as config_file:
			data = json.load(config_file)
		self.current_config = data
	def write_configs(self):
		with open(self.target, "w+") as f:
			json.dump(self.current_config, f,indent=4)
	def add_admin(self,user_id):
		self.current_config["default_admins"].append(user_id)
		self.write_configs()
	def remove_admin(self,user_id):
		if user_id in self.current_config["default_admins"]:
			self.current_config["default_admins"].remove(user_id)
			self.write_configs()