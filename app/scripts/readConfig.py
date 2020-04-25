# -*- coding: utf-8 -*-

##########################################################################################################################
## Script used for returning data about the configuration file.															##
## Also used to generate a new config file in the event there isn't an existing one.									##
##########################################################################################################################

# Required imports
import sys
#sys.path.insert(1, r'\app\scripts')
#import utilities
from . import utilities
import json, os

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
	removeCovers = False
	removeMKVTitle = False
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
			

			# General Settings
			if (config_data[10].lower().find("true") != -1):												# Determine if debug mode should enabled
				debug = True
			if (config_data[11].lower().find("true") != -1):												# Determine if only mkvs should be retained
				keepNonMkv = True
			if ((config_data[12].split('sorted_location = "')[1].split('"')[0]) != ""):
				sortedDir = config_data[12].split('sorted_location = "')[1].split('"')[0]
			
			# Config to remove mkv covers (with support for all, none, or only extras)
			if (config_data[13].lower().find("true extras") != -1):											# Config to remove mkv covers (extras only, check first)
				removeCovers = 2
			elif (config_data[13].lower().find("true") != -1):												# Config to remove mkv covers (all files)
				removeCovers = 1
			else:
				removeCovers = False																		# Otherwise skip removing covers

			temp_nonvid = config_data[15].split('non_video_files = "')[1].split('"')[0]						# Determine if non-video type files should be sorted, deleted, recycled or skipped.
			temp_bonus_folder = config_data[16].split('bonus_folder_name = "')[1].split('"')[0]

			# Config to remove mkv video titles (with support for all, none, or only extras)
			if (config_data[17].lower().find("true extras") != -1):											# extras only, check first
				removeMKVTitle = 2
			elif (config_data[17].lower().find("true") != -1):												# all files
				removeMKVTitle = 1
			else:
				removeMKVTitle = False																		# Otherwise skip removing title from video

			# Read from personalisation section
			if (config_data[20].lower().find("true") != -1):
				keyword_strip = True																			# Set to true
				
				split_temp = config_data[21].split('keywords = "')[1].split('"')[0]							# Get the full string between quotation marks.
				keywordsToStrip=split_temp.split(';')														# Split into list separating string by semicolon.

			# Read from rename settings
			spaceCharacter = config_data[25].split('space_character = "')[1].split('"')[0]



			# Check values are acceptable.
			if (utilities.checkExist(sortedDir) is False):
				if utilities.confirm('"Your desired output folder '+sortedDir+'" does not exist, attempt to create it?'):
					os.makedirs(sortedDir, mode=0o777, exist_ok=False)										# Create content directory
				else:
					raise Exception("Error -- You've opted not to create a new folder. Exception triggered as we cannot continue without an output location.")
					## Need some error handling here
					
				if (utilities.checkExist(sortedDir) is False):
					raise Exception('Tried to create this directory, but failed.') 							# Raise exception when failed to create requested directory.
			
			# Check non-video string is acceptable
			if temp_nonvid == "sort" or temp_nonvid == "skip" or temp_nonvid == "delete" or temp_nonvid == "recycle":
				nonVideoFiles = temp_nonvid
			else:
				print("Info -- Config: Unknown option for dealing with non-media files. Defaulting to skip.")
				nonVideoFiles = "skip"																		# Default to skip if preferences don't match a string.
			if temp_bonus_folder != "":
				bonusFolderName = temp_bonus_folder
			else:
				print("Info -- Config: Bonus folder string is not defined. Defaulting to 'Featurettes' for bonus output directory.")
				bonusFolderName = "Featurettes"																# Default "Featurettes" if no folder name given

			# Check match ratio
			if matchRatio > 1:
				raise Exception('Ratio is not formatted correctly. 0-1 and one decimal point only.') 		# Raise exception when match ratio is used incorrectly.
		
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
			a['removeCovers'] = removeCovers
			a['removeMKVTitle'] = removeMKVTitle
			a['sortedDirectory'] = sortedDir
			a['keywordsToStrip'] = keywordsToStrip
			a['nonVideoFiles'] = nonVideoFiles
			a['bonusFolderName'] = bonusFolderName

			# Rename settings
			a['spaceCharacter'] = spaceCharacter


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