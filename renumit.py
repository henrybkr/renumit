# -*- coding: utf-8 -*-

##########################################################################################################################
## ~ A Python script used for querying databases and renaming media accordingly based on personal preference and        ##
##   support for the Plex media servers.                                                                                ##
##                                                                                                                      ##
## ? What it does:                                                                                                      ##
##                                                                                                                      ##
## + Allows for user configuration via external file. Autogenerates when it doesn't exist. Example; match ratio.		##
## + Matches main content (Movie only currently) to a name and year. Other data often available not yet used.			##
## + Debug mode for individual comparison and confirmation before renaming.												##
## + Offers to create the desired output directory if it doesn't already exist.											##
## + Finds the main movie file even when there is more than one file in the main directory.								##
##                                                                                                                      ##
## ! Ideas/Issues/Concerns:                                                                                             ##
##                                                                                                                      ##
## - When more than one mkv in main directory, assuming that largest is the main content. Might be a problem.			##
##########################################################################################################################

#########################
# External imports

import os
import sys
import json

#########################
# Internal imports
#########################
# Include other path locations at runtime for easier access to package files, etc in different directories

sys.path.insert(1, r'app\api')
sys.path.insert(1, r'app\history')
sys.path.insert(1, r'app\scripts')
sys.path.insert(1, r'app\sorting')

import utilities, readConfig, configCheck # pylint: disable=import-error

#########################
# Application run order:
try:
	utilities.clear_win()																														# Clear the window on first launch.
	filePaths = utilities.intro(sys.argv[1:])																									# Run intro and review potential file paths provided to app
	
	configJSON = readConfig.read(os.path.dirname(os.path.abspath(__file__)))																	# Collect config json.
	configData = json.loads(configJSON)
	apisChecked = []																															# Will define what API's are working
	
	if(configJSON):
		print("-- Config file loaded ----------------------------------------------------------")
		utilities.writeLine()
		
		# Confirm api keys work
		apiCheckResult = configCheck.apiKeyLocator(configData['apiKeys'])
		#print(apiCheckResult)
		if apiCheckResult[0] == 1:
			print(apiCheckResult[1])
			# Perfect result. All keys present
		elif apiCheckResult[0] == 2:
			# One or more key not present. Acceptable result.
			print(apiCheckResult[1])
		else:
			# No keys present, fail.
			print(apiCheckResult[1])

		# Now lets check that the keys are functional.
		test = configCheck.apiTest("tmdb", configData['apiKeys'][0]['key'])
		#if test:
		#	print(test)
		# start renaming stuff!
	else:
		print("-- Hmm, problem with your configuration settings!")
	
	# Produce a menu to the user if no file paths provided.
	if not filePaths:
		# Make sure the menu is consistently displayed until a exit command is given.
		appContinue = True
		while appContinue == True:
			menuResult = utilities.menu()
			if menuResult[0] == 0:
				appContinue = False
			else:
				# Here we should launch the additional options in the menu. Might want to launch them from the menu utility itself, idk.
				print("\nMenu option was successfully chosen. However, functionality not currently there.")
				
	# Otherwise, begin making use of file paths.
	else:
		print("file paths present!")
		
		for current_path in filePaths:
			print(current_path)
	
	# End of application
	print("\n-- Info: Application closure.\n")
	os.system("pause")

except Exception as e:
	#os.system("pause")
	print("Sorry, looks like the app has failed somewhere...\nPlease provide the following information to me on my github page:\n")
	raise
	os.system("pause")