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

#
# overwrite debug mode
if args.debug:
  config['debug'] = True

#
# import plugins
plugins = utils.import_plugins()

#
# run plugins test() function if debug mode
if config['debug']:
	utils.debug('Executing test() from plugins:')
	for p in plugins.values():
		# check if test function exists
		if hasattr(p,'test'):
			utils.debug('- '+p.__name__+'.test() >> '+p.test())

#
# HTML header
html = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html charset=UTF-8" />
</head>
<body>
'''

#
# run plugins defined in cards and render HTML
for c in config['cards']:
	utils.debug('Executing plugin : %s' % c['title'] )
	# set variables for plugin name / module object / arguments
	plg = c['plugin']
	mod = plugins[ plg ]
	arg = c['arguments']
	# run plugin with arguments
	res = mod.run( arg )
	# render plugin result using plugin HTML template		
	out = utils.render( plg, res )
	# fix HTML block
	html += out + '\n'

#
# HTML footer
html += '''
</body>
</html>
'''

#
# output option set then write HTML content to file
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