import poloniex
import json
import threading
import smtplib

def loadConfigs(filename='config.json'):
	with open(filename, 'r') as f:
		configs = json.load(f)
	return configs	


def jsonToDf(json):
	dat = pd.DataFrame(json)
	# flip, reset index, drop extra row
	df = dat.iloc[::-1].reset_index().drop("index", axis=1)
	return df


def sendMsg(msg):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login("tifmrp1324ip@gmail.com", "wussgood$$$")
	server.sendmail("tifmrp1324ip@gmail.com", "6504006400@vtext.com", msg)
	server.sendmail("tifmrp1324ip@gmail.com", "alexmatthys@gmail.com", msg)
	server.quit() 

def write(msg):
	with open('log.txt', 'a+') as outfile:
		outfile.write(str(msg)+"\n")
