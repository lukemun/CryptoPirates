import poloniex
import json
import threading


def loadConfigs(filename='config.json'):
	with open(filename, 'r') as f:
		configs = json.load(f)
	return configs	

