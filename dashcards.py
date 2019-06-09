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
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
	<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
	<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
</head>
<body>
<div class="container">

	<div class="jumbotron">
	<h1>DashCards</h1> 
	<p>Create simple dashboard using your own cards</p> 
	</div>

	<div class="row">
'''

#
# run plugins defined in cards and render HTML
for c in config['cards']:
	utils.debug('Executing plugin : %s' % c['title'] )
	# set variables for plugin name / module object / arguments
	plg = c['plugin']
	mod = plugins[ plg ]
	arg = c['arguments']
	
	c['id'] = utils.randhash()
	# uid = utils.randhash()
	# tit = c['title']

	# run plugin with arguments
	res = mod.run( arg )
	# render plugin result using plugin HTML template		
	# out = utils.render( plg, {'id':uid,'plugin':plg,'title':tit}, res )
	out = utils.render( plg, c, res )
	# fix HTML block
	html += out + '\n'

#
# HTML footer
html += '''
	</div>
</div>

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