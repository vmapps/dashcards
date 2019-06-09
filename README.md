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
## Plugins structure
Plugins should respect following rules:
- been placed into 'plugins' directory
- plugin code could be named <plugin>.py
- plugin card could be name <plugin>.html
- have declared (at least) variables named : name, version, url, author, contact, description
- have declared (at least) functions named : test, run

## Plugins functions
Two functions are required for each plugin:
- test() : could be executed in debug mode 
- run() : main plugin function called by main program
- plugin should return JSON object after execution of run()
- JSON object returned is then rendered with Jinja2 using plugin HTML template
