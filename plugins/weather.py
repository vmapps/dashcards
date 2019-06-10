#!/usr/bin/env python3

import json
import random
import urllib

name = 'Weather plugin'
version = '0.1'
url = 'https://githib.com/vmapps/'
author = 'VMapps'
contact	= '31423375+vmapps@users.noreply.github.com'
description = 'Plugin to display weather card'

def test():
	return name + ' - v' + version

def run(args):

	# for demo purposes, this service relies on OpenWeatherMap services
	# check at https://openweathermap.org/api/

	# API call below is just sample and do not have any connection to the real API service!
	url = 'https://samples.openweathermap.org/data/2.5/weather?q=London,uk&appid=b6907d289e10d714a6e88b30761fae22'

	jobj = urllib.request.urlopen(url)
	data = json.loads( jobj.read() )

	return data
	
	