#!/usr/bin/python2.7
#coding:utf-8

import sys
import getopt
import re
sys.path.append('./lib')
# from scanner_class_mp import Scanner
from scanner_class_basic import Scanner
from scanner_class_pluginrunner import PluginMultiRunner
from listener_class import Listener
from consoler_class import Consoler
from consoleUser_class import WebUser
from plugin2sql import loadPlugins

# ----------------------------------------------------------------------------------------------------
# 
# ----------------------------------------------------------------------------------------------------
def show():
	print'''
   ██░ ██  ▄▄▄       ███▄ ▄███▓ ███▄ ▄███▓▓█████  ██▀███  
  ▓██░ ██▒▒████▄    ▓██▒▀█▀ ██▒▓██▒▀█▀ ██▒▓█   ▀ ▓██ ▒ ██▒
  ▒██▀▀██░▒██  ▀█▄  ▓██    ▓██░▓██    ▓██░▒███   ▓██ ░▄█ ▒
  ░▓█ ░██ ░██▄▄▄▄██ ▒██    ▒██ ▒██    ▒██ ▒▓█  ▄ ▒██▀▀█▄  
  ░▓█▒░██▓ ▓█   ▓██▒▒██▒   ░██▒▒██▒   ░██▒░▒████▒░██▓ ▒██▒
   ▒ ░░▒░▒ ▒▒   ▓▒█░░ ▒░   ░  ░░ ▒░   ░  ░░░ ▒░ ░░ ▒▓ ░▒▓░
   ▒ ░▒░ ░  ▒   ▒▒ ░░  ░      ░░  ░      ░ ░ ░  ░  ░▒ ░ ▒░
   ░  ░░ ░  ░   ▒   ░      ░   ░      ░      ░     ░░   ░ 
   ░  ░  ░      ░  ░       ░          ░      ░  ░   ░     
	'''

def usage():
	print "Usage: hammer.py [Auth] [Options] [Targets]\n"
	# print "\t-u --url: url address, like http://www.leesec.com/"
	print "[Auth]"
	print "\t-s --server: your hammer web server host address, like www.hammer.org"
	print "\t-t --token: token, find it in http://www.hammer.org/user.php"
	print "[Options]"
	print "\t-u --update-plugins: update new added plugins to web"
	print "\t-v --verbose: increase verbosity level"
	print "\t   --threads: max number of process, default cpu number"
	print "\t-h: help"
	print "[Targets]"
	print "\t-T --target: target, can be an ip address, an url or an iprange"
	print "\t   --no-gather: do not use information gather module"
	print "\t   --gather-depth: information gather depth, default 1"
	print "\t-p --plugin: run a plugin type scan"
	print "\t   --plugin-arg: plugin argus"
	print "\t-l --listen: listen mode"
	print "\t   --max-size: scan pool max size, default 50"
	print "\t-c --console: console mode"
	print "[Examples]"
	print "\thammer.py -s www.hammer.org -t 3r75... -u plugins/Info_Collect/"
	print "\thammer.py -s www.hammer.org -t 3r75... -T http://testphp.vulnweb.com"
	print "\thammer.py -s www.hammer.org -t 3r75... -p plugins/System/dnszone.py -T vulnweb.com"
	print "\thammer.py -s www.hammer.org -t 3r75... -l"
	sys.exit(0)

def main():

	try :
		opts, args = getopt.getopt(sys.argv[1:], "hvlcs:t:u:T:p:",['help','verbose=','server=','token=','update-plugins=','target=','plugin=','plugin-arg=','no-gather','gather-depth=','threads=','listen','console'])
	except getopt.GetoptError,e:
		print 'getopt.GetoptError',e
		usage()

	# default arguments
	_url = None
	_server = None
	_token = None
	# _gather_flag = True
	_listen = False
	_console = False
	_gather_depth = 1
	_vv = 'INFO'
	_plugin_arg=None
	_threads = None

	for opt, arg in opts:
		if opt in ('-h','--help'):
			usage()
		elif opt in ('-v'):
			_vv = 'DEBUG'
		elif opt in ('--no-gather'):
			# _gather_flag = False
			_gather_depth = 0
		elif opt in ('--gather-depth'):
			_gather_depth = int(arg)
		elif opt in ('-s','--server'):
			_server = arg
		elif opt in ('-t','--token'):
			_token = arg
		elif opt in ('-u','--update-plugins'):
			if arg:
				_pluginpath = arg
			else:
				_pluginpath = 'plugins/'
		elif opt in ('--threads'):
			_threads = int(arg)
		elif opt in ('-p','--plugin'):
			_plugin = arg
		elif opt in ('--plugin-arg'):
			_plugin_arg = arg
		elif opt in ('-T','--target'):
			_target = arg
		elif opt in ('-l','--listen'):
			_listen = True
		elif opt in ('-c','--console'):
			_console = True
		else:
			pass

	user = WebUser()
	if user.server and user.token:
		_server = user.server
		_token = user.token

	if _console:
		cn = Consoler()
		cn.run()

	elif _server and _token:
		show()
		if '_pluginpath' in dir():
			# print '_pluginpath=',_pluginpath
			# print '_server=',_server
			# print '_token=',_token
			loadPlugins(_pluginpath,_server,_token)

		elif '_target' in dir():
			# plugin type scan
			if '_plugin' in dir():
				sn = PluginMultiRunner(server=_server,token=_token,target=_target,loglevel=_vv,threads=_threads,pluginfilepath=_plugin,pluginargs=_plugin_arg)
				sn.initInfo()
				sn.scan()
			else:
				sn = Scanner(server=_server,token=_token,target=_target,threads=_threads,loglevel=_vv,gatherdepth=_gather_depth)
				sn.initInfo()
				sn.infoGather(depth=_gather_depth)
				sn.scan()

		elif _listen:
			li = Listener(server=_server, token=_token, loglevel=_vv)
			li.run()
		
	else:
		usage()
# ----------------------------------------------------------------------------------------------------
# 
# ----------------------------------------------------------------------------------------------------
if __name__=='__main__':
	main()