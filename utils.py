import poloniex
import json
import threading


def loadConfigs(filename='config.json'):
	with open(filename, 'r') as f:
		configs = json.load(f)
	return configs	


def json_to_df(json):
	dat = pd.DataFrame(json)
	# flip, reset index, drop extra row
	df = dat.iloc[::-1].reset_index().drop("index", axis=1)
	return df