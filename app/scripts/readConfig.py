# -*- coding: utf-8 -*-

##########################################################################################################################
## Script used for returning data about the configuration file.															##
## Also used to generate a new config file in the event there isn't an existing one.									##
##########################################################################################################################

# Required imports
import sys
sys.path.insert(1, r'\app\scripts')
import utilities
import json

# Read from the config file if it exists, else generate it.
def read(path):

	configPath = path+r"\\data\\preferences.config"																# Expected relative path to the renumit config file.
	config_file = ""																						# Empty for now.
	
	# User configuration variables
	##############################
	apiKeys = []																							# 0 = TMDb, 1 = TVDb, 2 = OMDb
	matchRatio = 0
	debug = False
	keepNonMkv = False
	sortedDir = ""
	removeCoverTitles = False
	keyword_strip = False
	keywordsToStrip = []
	
	
	# First step, check that an existing config file exists
	try:
		config_file = open(configPath, "r")																	# Attempt to open the config file
	
	# If we can't find the config file, return with the result of not found.
	except FileNotFoundError:																				# When file is not found
		#print("Warning_101: No config file found. Creating one now!")
		return 1
	
	# Any other exception that might be found, return error.
	except:
		print("Unknown Error!")
		return 2
	
	if config_file:
		try:
			config_data = config_file.read().split("\n")													# Read the config file and split on each new line, creating an array.
			config_file.close()																				# Now that data is stored, close file.
			
			# Note: API Key will display as '' if empty. Issue will occur if user changes config file format.
			
			apiKeys.append(config_data[3].split('TMDb = "')[1].split('"')[0])								# Append TMDb api key to list
			apiKeys.append(config_data[4].split('TVDb = "')[1].split('"')[0])								# Append TVDb api key to list
			apiKeys.append(config_data[5].split('OMDb = "')[1].split('"')[0])								# Append OMDb api key to list
			
			#print(config_data[9].split('match_rate = "')[1].split('"')[0])
			
			matchRatio = float(config_data[9].split('match_rate = "')[1].split('"')[0])						# Collect match ratio, convert to float
			
			if (config_data[10].lower().find("true") != -1):												# Determine if debug mode should enabled
				debug = True
			if (config_data[11].lower().find("true") != -1):												# Determine if only mkvs should be retained
				keepNonMkv = True
			if ((config_data[12].split('sorted_location = "')[1].split('"')[0]) != ""):
				sortedDir = config_data[12].split('sorted_location = "')[1].split('"')[0]
			if (config_data[13].lower().find("true") != -1):												# Config to remove mkv covers
				removeCoverTitles = True
			# Read from personalisation section
			if (config_data[16].lower().find("true") != -1):
				
				keyword_strip = True			# Set to true
				
				split_temp = config_data[17].split('keywords = "')[1].split('"')[0]							# Get the full string between quotation marks.
				keywordsToStrip=split_temp.split(';')														# Split into list separating string by semicolon.
				
			
			
			# Check values are acceptable.
			if (utilities.checkExist(sortedDir) is False):
				if utilities.confirm('"Your desired output folder '+sortedDir+'" does not exist, attempt to create it?'):
					os.makedirs(sortedDir, mode=0o777, exist_ok=False)										# Create content directory
				if (utilities.checkExist(sortedDir) is False):
					raise Exception('Tried to create this directory, but failed.') 							# Raise exception when failed to create requested directory.
			if matchRatio > 1:
				raise Exception('Ratio is not formatted correctly. 0-1 and one decimal point only.') 		# Raise exception when match ratio is used incorrectly.
			

			#Currently not needed. Potential debug mode feature.
			"""
			# Check if all API keys are present.	
			num = 0
			for x in apiKeys:
				if x is not "":
					num+=1																					# Itterate num value by 1 (number of api keys found)
			if num == len(apiKeys):																			# If all keys are found
				print(utilities.line+"\n--------------------- Config file loaded - All keys found! ---------------------\n"+utilities.line+"\n")
			elif (num == 0):
				print(utilities.line+"\n---------------------- Config file loaded - 0 keys found! ----------------------")
				raise Exception('No API keys present. Please make sure there is at least one!')
			else:																							# If one ore more key missing
				print(utilities.line+"\n--------------- Config file loaded - Missing "+str((len(apiKeys))-num)+" API key(s) though! --------------\n"+utilities.line+"\n")
			
			# Output full config info if this debug mode is enabled
			if (debug):
				print("full config text:\n")
				for x in config_data:
					print(x)
			"""
		
			# Create the dict object and begin populating it with data to later return.
			a = {}
			
			# apiKeys
			a['apiKeys'] = []	# Initiate as empty
			a['apiKeys'].append({'name': 'TMDb','key': apiKeys[0] })
			a['apiKeys'].append({'name': 'TVDb','key': apiKeys[1] })
			a['apiKeys'].append({'name': 'OMDb','key': apiKeys[2] })

			# Other user settings
			a['matchRate'] = matchRatio
			a['debugMode'] = debug
			a['keepNonMkv'] = keepNonMkv
			a['removeCoverTitles'] = removeCoverTitles
			a['sortedDirectory'] = sortedDir
			a['keywordsToStrip'] = keywordsToStrip

			# Return in json format
			jsonOutput = json.dumps(a)
			return jsonOutput
			
		
		except:
			print("Whoops, error in readConfig.read()")
			raise
			return 3

##

## Note to self, the newConfig function could do with testing.

##

def newConfig(path):
	try:
	
		config_file = open("renumit.config", "w+")
		config_file.write('### RENUMIT CONFIG FILE ###\n\n# API Keys\nTMDb = ""\nTVDb = ""\nOMDb = ""\n\n\n# Settings\nmatch_rate = 0.875\ndebug = False\nkeep_non_mkv = False\nsorted_location = ""\nremove_covers_titles = true\n\n# Keyword Settings #\nstripped = false\nkeywords = ""')
		print(utilities.line+'\nConfig file created. Please edit it without reformatting. File located here: "'+os.path.realpath(config_file.name)+'"')
		config_file.close
	except:
		print("Error_101: Failed to create or write to config file. Check write permissions.")