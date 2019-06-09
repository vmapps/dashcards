# dashcards
Build HTML dashboard using user-defined cards

## Purpose 
Purpose of this very simple tool is to :
- build a HTML dashboard using cards 
- cards are kind of plugins that user can develop
- cards can be called multiple times

## Requirements
Following python modules are required :
- [jinja2](http://jinja.pocoo.org/)

Modules could be installed using following commands:
```
$ pip install -r requirements.txt
```
## Configuration
Settings have to be changed using file **config-template.json** :
```
# enable/disable debug mode
"debug": [true|false]

# cards (array of settings)
{
	"title": "<name of the card>",
	"plugin": "<plugin to be used>",
	"arguments": [<arguments>,<sent>,<to>,<plugin>]
}
```
Then rename template file as config.json
```
mv config-template.json config.json
```
## Usage
```
usage: dashcards.py [-h] [-d] [-c <filename>] [-o <filename>]

optional arguments:
  -h, --help     show this help message and exit
  -d, --debug    force debug mode (not used yet)
  -c <filename>  config file name (defaut: config.json)
  -o <filename>  output file name
```
## Plugins 
#### Structure
Plugins should respect following rules:
- been placed into 'plugins' directory
- plugin code could be named <plugin>.py
- plugin card could be name <plugin>.html
- have declared (at least) variables named : name, version, url, author, contact, description
- have declared (at least) functions named : test, run

#### Functions
Two functions are required for each plugin:
- test() : could be executed in debug mode 
- run() : main plugin function called by main program
- plugin should return JSON object after execution of run()
- JSON object returned is then rendered with Jinja2 using plugin HTML template

#### Rendering
Jinja2 templating module is used to render HTML :
- JSON object returned by plugin is sent to template as variable 'render.xxx'
- some main variables are also available in template : 'card.id' (random) and 'card.title' (fron card config)

## Sample plugin
#### Python code
```
#!/usr/bin/env python3

import json

name = 'Sample plugin'
version = '0.1'
url = 'https://githib.com/vmapps/'
author = 'VMapps'
contact	= '31423375+vmapps@users.noreply.github.com'
description = 'Sample plugin for demo'

def test():
	return name + ' - v' + version

def run(args):
	return { 'name':name, 
			'version':version, 
			'description':description, 
			'arg0':args[0], 
			'arg1':args[1] 
			}
```

#### HTML template
```
<div class="sample" id="{{ card.id }}">
	<p>{{ card.title }}</p>
	<ul>
		<li>Plugin name : {{ render.name }}</li>
		<li>Plugin version : {{ render.version }}</li>
		<li>Plugin description : {{ render.description }}</li>
		<li>Plugin argument #0 : {{ render.arg0 }}</li>
		<li>Plugin argument #1 : {{ render.arg1 }}</li>
	</ul>
</div>
```

#### Card configuration
```
{
	"title": "Test Sample",
	"plugin": "sample",
	"arguments": ["foo","bar"]
}
```

#### HTML Output
```
<div class="weather">
        <p>Plugin name : Sample plugin</p>
        <p>Plugin version : 0.1</p>
        <p>Plugin description : Sample plugin for demo</p>
        <p>Plugin argument #0 : foo</p>
        <p>Plugin argument #1 : bar</p>
</div>
```
