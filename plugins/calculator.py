#!/usr/bin/env python3

import json

name = 'Calculator plugin'
version = '0.1'
url = 'https://githib.com/vmapps/'
author = 'VMapps'
contact	= '31423375+vmapps@users.noreply.github.com'
description = 'Plugin to display calc simple result'

def test():
	return name + ' - v' + version

def run(args):

	res = { 'add':args[0]+args[1] }

	return res