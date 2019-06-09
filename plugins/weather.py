#!/usr/bin/env python3

import json

name = 'Weather plugin'
version = '0.1'
url = 'https://githib.com/vmapps/'
author = 'VMapps'
contact	= '31423375+vmapps@users.noreply.github.com'
description = 'Plugin to display weather card'

def test():
	return name + ' - v' + version

def run(args):
	
	res = { 'location':args[0], 'temperature':23, 'units':args[1] }

	return res
	
	