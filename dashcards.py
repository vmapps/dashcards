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
parser.add_argument('-t', help='templates directory name (defaut: templates)', metavar='<filename>', action='store')
parser.add_argument('-o', help='output file name', metavar='<filename>', action='store')
args = parser.parse_args()

#
# checks arguments and options

file_cfg = args.c if args.c else os.path.dirname(__file__) + '/config.json'
dir_tmpl = args.t if args.t else os.path.dirname(__file__) + '/templates'
file_out = args.o if args.o else None

#
# open configuration file
config = json.loads( utils.getfile(file_cfg) )

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
html = utils.getfile(dir_tmpl+'/_header.html')

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
	out = utils.render( dir_tmpl+'/'+plg+'.html', c, res )
	# fix HTML block
	html += '\n<!-- Plugin %s id=%s -->\n' % (plg,c['id'])
	html += '<div class="col">'
	html += out
	html += '</div>'
	html += '<!-- Plugin %s id=%s -->\n' % (plg,c['id'])

#
# HTML footer
html += utils.getfile(dir_tmpl+'/_footer.html')

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