from exceptions import ConfigError
import json
import os

class config:
	def __init__(self):
		self.target = "config.json"
		self.current_config = {}
		self.template_config = {
			"bot_token":"",
			"server_script":"",
			"server_args":[]
		}
		if not os.path.isfile(self.target):
			with open(self.target, "w+") as f:
				json.dump(self.template_config,f)
	def read_configs(self):
		if not os.path.isfile(self.target):
			raise ConfigError(f"Config file at {self.target} not found.")
		with open(self.target, "r") as config_file:
			data = json.load(config_file)
		self.current_config = data
	def write_configs(self):
		with open(self.target, "w+") as f:
			json.dump(self.current_config, f)