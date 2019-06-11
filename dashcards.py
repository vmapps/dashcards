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
parser.add_argument('-t', help='templates directory name (defaut: templates)', metavar='<dirname>', action='store')
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
if os.path.isfile(dir_tmpl+'/_header.html'):
	html = utils.getfile(dir_tmpl+'/_header.html')

#
# run plugins defined in cards and render HTML
for c in config['cards']:
	# set variables for plugin name / module object / arguments
	plg = c['plugin']
	mod = plugins[ plg ]
	arg = c['arguments']
	tpl = plg
	# add unique id to plugin	
	c['id'] = utils.randhash()
	# run plugin with arguments
	utils.debug('Executing plugin : %s' % c['title'] )
	res = mod.run( arg )
	# check if any alternative template should b e used
	if c.get('template'): tpl = c['template']
	if res.get('template'): tpl = res['template']
	# render plugin result using plugin HTML template		
	# out = utils.render( plg, {'id':uid,'plugin':plg,'title':tit}, res )
	utils.debug('Rendering template : %s' % dir_tmpl+'/'+tpl+'.html' )
	out = utils.render( dir_tmpl+'/'+tpl+'.html', c, res )
	# fix HTML block
	html += '\n<!-- Plugin %s id=%s -->\n' % (plg,c['id'])
	html += '<div class="col m-2">'
	html += out
	html += '</div>'
	html += '<!-- Plugin %s id=%s -->\n' % (plg,c['id'])

#
# HTML footer
if os.path.isfile(dir_tmpl+'/_footer.html'):
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