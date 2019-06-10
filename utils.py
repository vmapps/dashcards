#!/usr/bin/env python3
# -*- coding: Utf-8 -*

#
# imports required modules
# --------------------------------------------------
import __main__

import importlib
import jinja2
import os
import pkgutil
import sys
import uuid

#
# global variables
# --------------------------------------------------
plugname = 'plugins'
plugpath = os.path.dirname(__file__)+'/'+plugname
tmplpath = os.path.dirname(__file__)+'/templates'

#
# debug
# --------------------------------------------------
def debug(buffer):
	if __main__.config['debug']:
		sys.stderr.write( '[DEBUG] %s\n'%buffer )
	else:
		pass

#
# random hash
def randhash():
	return uuid.uuid4().hex

#
# read file content
def getfile(filename):
	try:
		with open(filename,'r') as fh:
			buffer = fh.read()
		fh.close()
		return buffer
	except Exception as e:
		sys.stderr.write( '[ERROR] reading configuration file %s\n' % file_cfg )
		sys.stderr.write( '[ERROR] %s\n' % str(e) )
		sys.exit(1)

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
def render(template,card,render):
	#
	# open template file
	tpl = jinja2.Template( getfile(tmplpath+'/'+template+'.html') )

	# render template with data
	html = tpl.render( card=card,render=render )

	return html