#!/usr/bin/env python3
# -*- coding: Utf-8 -*

#
# imports required modules
import argparse
import json
import os
import sys
import utils

#
# set command-line arguments and parsing options
parser = argparse.ArgumentParser()
parser.add_argument('-d','--debug', help='force debug mode (not used yet)', default=False, action='store_true')
parser.add_argument('-c', help='config file name (defaut: config.json)', metavar='<filename>', action='store')
parser.add_argument('-o', help='output file name', metavar='<filename>', action='store')
args = parser.parse_args()

#
# checks arguments and options

file_cfg = args.c if args.c else os.path.dirname(__file__) + '/config.json'
file_out = args.o if args.o else None

#
# open configuration file
try:
  with open( file_cfg,'r') as fh:
    config = json.load(fh)
  fh.close()
except Exception as e:
  sys.stderr.write( '[ERROR] reading configuration file %s\n' % file_cfg )
  sys.stderr.write( '[ERROR] %s\n' % str(e) )
  sys.exit(1)

if args.debug:
  config['debug'] = True

plugins = utils.import_plugins()

utils.debug('Executing test() from plugins:')
for p in plugins.values():
	if hasattr(p,'test'):
		utils.debug('- '+p.__name__+'.test() >> '+p.test())

html = ''
for c in config['cards']:
	utils.debug('Executing plugin : %s' % c['title'] )

	plg = c['plugin']
	mod = plugins[ plg ]
	arg = c['arguments']
	
	res = mod.run( arg )
	out = utils.render( plg, res )

	html = html + out + '\n'

# if output option set then write HTML content to file
if file_out is not None:
	try:
		with open( file_out,'w') as fh:
			fh.write( html )
			fh.close()
	except Exception as e:
		sys.stderr.write( '[ERROR] opening output file %s\n' % file_out )
		sys.stderr.write( '[ERROR] %s\n' % str(e) )
		sys.exit(1)
else:
	print( html )

#
# end