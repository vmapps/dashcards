#!/usr/bin/env python3

import json
import urllib.request

name = 'Finance Quote plugin'
version = '0.1'
url = 'https://githib.com/vmapps/'
author = 'VMapps'
contact	= '31423375+vmapps@users.noreply.github.com'
description = 'Sample to display finance quotes'

def test():
	return name + ' - v' + version

def run(args):
	
	# for demo purposes, this service relies on Financial Modeling Prep services
	# check at https://financialmodelingprep.com/developer/docs/

	url = 'https://financialmodelingprep.com/api/v3/stock/real-time-price/' + args[1]

	jobj = urllib.request.urlopen(url)
	data = json.loads( jobj.read() )

	data['price'] = '%.2f' % data['price']
	data['name'] = args[0] 

	return data
	
	