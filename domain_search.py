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



def valid(app):
	if app in Dict or app in DictAll:
		return True
	return False

def curl(app):
	if valid(app) == False:
		return
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

def readWords():
	readWordsFull()
	readWordsHelper('2.txt')
	readWordsHelper('3.txt')
	readWordsHelper('4.txt')
	readWordsHelper('5.txt')

Dict = Set([])
DictAll = Set([])

def readWordsHelper(file):
	with open(file, 'rb') as csvfile:
		wordreader = csv.reader(csvfile, delimiter=',')
		for box in wordreader:
			for word in box:
				Dict.add(word)

def readWordsFull():
	with open('all.txt', 'rb') as csvfile:
		wordreader = csv.reader(csvfile)
		for box in wordreader:
			for word in box:
				if len(word) < 9:
					DictAll.add(word)

if __name__ == "__main__":
	from sys import argv
	myargs = getopts(argv)
	if '-app' in myargs:
		curl(myargs['-app'])
	else:
		readWords()
		amazon = list(string.ascii_lowercase)
		for i in range(len(amazon)):
			for j in range(len(amazon)):
				two = amazon[i]+amazon[j]
				curl(two)
				for k in range(len(amazon)):
					three = two + amazon[k]
					curl(three)
					for m in range(len(amazon)):
						four = three + amazon[m]
						curl(four)
						for n in range(len(amazon)):
							five = four + amazon[n]
							curl(five)


