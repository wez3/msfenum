#!/usr/bin/python

import logging, time, json, argparse, fileinput
from os import listdir, system, path, makedirs
from sys import exit

def loadConfig():
	"""
	Loads the configuration file(s)
	"""
	
	try:
		with open('config') as f:
			return json.load(f)
	except:
		logging.error("Failed to load config")


def validateModuleConfig(modules, modulesconfig, config):
	"""
	Validates the module config
	"""
	modulesfolder = config.get('modulesfolder')
	missing = []
	for module in modules:
		modulename = module.split("/")[-1]
		if (not path.isfile(path.join(modulesfolder,modulename))):
			missing.append(modulename)			
	if missing:
		logging.warning("missing the following module(s): " + "".path.join(missing))


def generateRcs(targets, threads, currentTime, config):
	"""
	Compiles all module configurations into one RC file
	"""
	modulesfolder = config.get('modulesfolder')
	postmodule = "spool off\n\n"
	premodule = "spool "+ config.get('logsfolder') + "/"
	modules = config.get('modules')
	modulesconfig = [f for f in listdir(modulesfolder) if path.isfile(path.join(modulesfolder, f))]

	validateModuleConfig(modules, modulesconfig, config)

	if threads == None:
		threads = str(config.get('defaultthreads'))

	rcfile = ""
	for target in targets:
		for module in modules:
			modulename = module.split("/")[-1]
			if (path.isfile(path.join(modulesfolder,modulename))):
				rcfile += "setg threads " + str(threads) + "\n"
				rcfile += premodule + currentTime + "/" + modulename + ".log\n"
				rcfile += "use " + module + "\n"
				rcfile += open(path.join(modulesfolder,modulename),'r').read().replace("%IP%", target)
				rcfile += postmodule
	rcfile += "exit -y\n"
	rcoutput = open(config.get('logsfolder') + '/' + currentTime + '/file.rc', 'w')
	rcoutput.write(rcfile)
	rcoutput.close()


def runRcs(currentTime, config):
	"""
	Runs metasploit commands and prints output
	"""
	logsfolder = config.get('logsfolder')
	
	logging.info('--- Starting msfconsole ---')
	system('msfconsole -r ' + logsfolder + '/' + currentTime + '/file.rc')
	logging.info('--- Msfconsole done ---')


def getSuccessful(currentTime, config):
	"""
	Prints all [+] entries in the log in context. 
	"""
	logsfolder = config.get('logsfolder')
	
	logging.info('--- Summary of discovered results ---')
	for f in listdir(logsfolder + '/'+ currentTime):
		
		if f.endswith(".log"):
			logging.info('- Module: ' + f.rsplit('.', 1)[0])
			result = system('grep [+] ' + logsfolder + '/' + currentTime + '/' + f)
			
			if result == 256 or result == 0: # No results end in a 256 or 0 print
				logging.info("[-] No results")
			else:
				logging.info(result)
				
	logging.info('--- Msfenum done ---')


def ascii():
	"""
	We need some ASCII
	"""
	print(r"""
	             . --- .
	           /        \
	          |  O  _  O |
	          |  ./   \. |
	          /  `-._.-'  \
	        .' /         \ `.
	    .-~.-~/           \~-.~-.
	.-~ ~    |             |    ~ ~-.
	`- .     |             |     . -'
	     ~ - |             | - ~
	         \             /
	       ___\           /___
	       ~;_  >- . . -<  _i~
	          `'         `'
	      By: @wez3forsec, @rikvduijn
	      """)


if __name__ == '__main__':
	# Load config with default settings
	config = loadConfig()
	
	# Define variables
	logsfolder = config.get('logsfolder')
	logfile= "msfenum.log"
	targets = []
	currentTime = int(time.time())
	currentDir = logsfolder + '/' + str(currentTime)
	threads = None

	# Define logger settings
	logging.basicConfig(filename=logfile, level=logging.INFO)
	logging.getLogger().addHandler(logging.StreamHandler())
	ascii()
	logging.info('--- Starting msfenum ---')

	# Create current run directory
	logging.info('[*] Saving msfenum logs in: ' + currentDir)
	makedirs(currentDir)

	# Parse command line arguments
	parser = argparse.ArgumentParser(description="Metasploit framework auto enumeration script")
	parser.add_argument('-t', '--threads', nargs='?', help="Number of threads", type=int)
	parser.add_argument('files', metavar='TARGET_FILE', help='File containing targets')
	args = parser.parse_args()

	# Check if target file is accessible and load it
	if not path.isfile(args.files):
		exit('Target file does not exist')
	for target in fileinput.input(files=args.files if len(args.files) > 0 else ('-', )):
		targets.append(target)

	# Check if threads are specified.
	if args.threads is not None:
		threads = args.threads

	

	# Run the script
	generateRcs(targets, threads, str(currentTime), config)
	runRcs(str(currentTime), config)
	getSuccessful(str(currentTime), config)

