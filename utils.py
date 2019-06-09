#!/usr/bin/env python3
# -*- coding: Utf-8 -*

#
# imports required modules
# --------------------------------------------------
import importlib
import jinja2
import os
import pkgutil
import sys
import __main__
#
# global variables
# --------------------------------------------------
plugname = 'plugins'
plugpath = os.path.dirname(__file__)+'/'+plugname

#
# debug
# --------------------------------------------------
def debug(buffer):
	if __main__.config['debug']:
		sys.stderr.write( '[DEBUG] %s\n'%buffer )
	else:
		pass

#
# import modules
# --------------------------------------------------
def import_plugins():

	plugdict = {}

	debug('search for plugins into directory '+plugpath)
	for (_, name, _) in pkgutil.iter_modules([plugpath]):
		try:
			mod = importlib.import_module('.'+name,package=plugname)
			debug('- found plugin %s (%s - %s)' % (name,getattr(mod,'name'),getattr(mod,'version')))
			plugdict[name] = mod
		except ImportError as err:
			debug('- import error with %s' % name) 

	return plugdict

#
# render plugins template
# --------------------------------------------------
def render(template,data):
	#
	# open template file
	try:
		with open(plugpath+'/'+template+'.html','r') as fh:
			tpl = jinja2.Template(fh.read())
		fh.close()
	except Exception as e:
		sys.stderr.write( '[ERROR] reading template file %s\n' % template )
		sys.stderr.write( '[ERROR] %s\n' % str(e) )
		sys.exit(1)

	# render template with data
	html = tpl.render( render=data )

	return html