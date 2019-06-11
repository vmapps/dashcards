#!/usr/bin/env python3

import json
import shutil

name = 'System plugin'
version = '0.1'
url = 'https://githib.com/vmapps/'
author = 'VMapps'
contact	= '31423375+vmapps@users.noreply.github.com'
description = 'Plugin to display system info'

def test():
	return name + ' - v' + version

def run(args):

	total, used, free = shutil.disk_usage( args[0] )

	return { 'disk':args[0], 'total':(total//(2**30)), 'used':(used//(2**30)), 'free':(free//(2**30)), 'units':'GB' }
