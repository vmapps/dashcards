#!/usr/bin/env python3

import json

name = 'Sample plugin'
version = '0.1'
url = 'https://githib.com/vmapps/'
author = 'VMapps'
contact	= '31423375+vmapps@users.noreply.github.com'
description = 'Sample plugin for demo'

def test():
	return name + ' - v' + version

def run(args):
	
	return { 'name':name, 
			'version':version, 
			'description':description, 
			'arg0':args[0], 
			'arg1':args[1] 
			}

	return res
	
	