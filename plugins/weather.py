#!/usr/bin/env python3

import json
import random
name = 'Weather plugin'
version = '0.1'
url = 'https://githib.com/vmapps/'
author = 'VMapps'
contact	= '31423375+vmapps@users.noreply.github.com'
description = 'Plugin to display weather card'

def test():
	return name + ' - v' + version

def run(args):
	
	temp = 20 + random.randint(0,20)
	if args[1]=='F':
		temp = round(temp*9/5+32)

	res = { 'location':args[0], 'temperature':temp, 'units':args[1] }

	return res
	
	