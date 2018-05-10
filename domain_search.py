#!/usr/bin/python

import sys, getopt
import requests
import json
import string
import time
import csv
from sets import Set

def getopts(argv):
	opts = {}  # Empty dictionary to store key-value pairs.
	while argv:  # While there are arguments left to parse...
		if argv[0][0] == '-':  # Found a "-name value" pair.
			opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
		argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
	return opts

def curl(app):
	url = "https://domain-registry.appspot.com/check?domain=" + app + ".app"
	headers = {
		'origin': 'https://get.app',
		'accept-encoding': 'gzip, deflate, br',
		'accept-language': 'en-US,en;q=0.9', 
		'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1', 
		'accept': '*/*', 
		'referer': 'https://get.app/', 
		'authority': 'domain-registry.appspot.com', 
		'dnt': '1',
	}
	resp = requests.get(url,headers=headers)
	if resp.status_code == 200:
		data = json.loads(resp.content)
		if data["available"] != False:
			print app + ".app"

def findDomains():
	with open('all.txt', 'rb') as csvfile:
		wordreader = csv.reader(csvfile)
		for box in wordreader:
			for word in box:
				if len(word) >= minArgValue and len(word) <= maxArgValue:
					curl(word)



maxArgValue = 0
minArgValue = 0
hasMaxArg = False
hasMinArg = False
imaginary = "I hope you are not looking for imaginary domains"

if __name__ == "__main__":
	from sys import argv
	myargs = getopts(argv)
	if '-app' in myargs:
		curl(myargs['-app'])
	else:
		if '-max' in myargs:
			maxArgValue = int(myargs['-max'])
			hasMaxArg = True
		if '-min' in myargs:
			minArgValue = int(myargs['-min'])
			hasMinArg = True

		if hasMaxArg and hasMinArg:
			if minArgValue > maxArgValue:
				print imaginary
				sys.exit()
			elif maxArgValue < 1 or minArgValue < 1:
				print imaginary
				sys.exit()
		elif hasMaxArg:
			if maxArgValue < 1:
				print imaginary
				sys.exit()
			minArgValue = 1
		elif hasMinArg:
			if minArgValue < 1:
				print imaginary
				sys.exit()
			maxArgValue = 8
		else:
			minArgValue = 1
			maxArgValue = 8
		findDomains()
