#!/usr/bin/env python3

import sys, getopt
import requests, concurrent.futures
import json, string, csv
import random
import asyncio
from aiohttp import ClientSession

def getopts(argv):
	opts = {}  # Empty dictionary to store key-value pairs.
	while argv:  # While there are arguments left to parse...
		if argv[0][0] == '-':  # Found a "-name value" pair.
			opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
		argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
	return opts

async def fetch(url, session):
	async with session.get(url) as response:
		return await response.read()

async def bound_fetch(sem, app, url, session):
	# Getter function with semaphore.
	async with sem:
		return (app, await fetch(url, session))

async def run():
	url = "https://domain-registry.appspot.com/check?domain={}.app"
	tasks = []
	sem = asyncio.Semaphore(1000)
	async with ClientSession() as session:
		for app in Words:
			task = asyncio.ensure_future(bound_fetch(sem, app, url.format(app), session))
			tasks.append(task)
		return await asyncio.gather(*tasks)


Words = set()
def findDomains():
	with open('all.txt', 'rt', encoding='utf8') as csvfile:
		wordreader = csv.reader(csvfile)
		for box in wordreader:
			for word in box:
				if len(word) >= minArgValue and len(word) <= maxArgValue:
					Words.add(word)
	loop = asyncio.get_event_loop()
	future = asyncio.ensure_future(run())
	done = loop.run_until_complete(future)
	for response in done:
		if json.loads(response[1])["available"] != False:
			print (response[0])

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
				print (imaginary)
				sys.exit()
			elif maxArgValue < 1 or minArgValue < 1:
				print (imaginary)
				sys.exit()
		elif hasMaxArg:
			if maxArgValue < 1:
				print (imaginary)
				sys.exit()
			minArgValue = 1
		elif hasMinArg:
			if minArgValue < 1:
				print (imaginary)
				sys.exit()
			maxArgValue = 8
		else:
			minArgValue = 1
			maxArgValue = 8
		findDomains()
