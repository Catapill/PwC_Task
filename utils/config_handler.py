# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 17:54:16 2024

@author: adamw
"""
from yaml import safe_load

class ConfigHandler:
    def __init__(self, config_folder):
        # Initialise config folder.
        self.config_folder = config_folder
        
    def read_config(self, config_name):
        # Open config.
        with open(f"../{self.config_folder}/{config_name}.yml", mode="r", encoding="utf-8-sig") as config_file:
            content = config_file.read().replace("\t", "    ")
            config = safe_load(content)
        return config