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

import utilities, readConfig, configCheck, filenameReview, renamer # pylint: disable=import-error

#########################
# Application run order:
try:
	utilities.clear_win()																										# Clear the window on first launch.
	filePaths = utilities.intro(sys.argv[1:])																					# Run intro and review potential file paths provided to app
	
	configJSON = readConfig.read(os.path.dirname(os.path.abspath(__file__)))													# Collect config json.
	configData = json.loads(configJSON)
	apiKeychain = []
	debugMode = False																											# Empty now but used for what API's are working
	
	if not(configJSON):
		print("-- Hmm, problem with your configuration settings!")
	else:
		print("-- Config file loaded ----------------------------------------------------------")
		utilities.writeLine()
		
		# Confirm api keys work
		apiCheckResult = configCheck.apiKeyAvailable(configData['apiKeys'])														# Launch apiKeyAvailable function
		
		# Enable debug flag if required														
		debugMode = bool(configData['debugMode'])
		
		if apiCheckResult[0] == 0:
			# No keys present, fail.
			print(apiCheckResult[1])
		else:
			# If at least one api key is found, test which ones are working.
			print(apiCheckResult[1])																							# Output api key info

			# Now lets check that the keys are functional.
			tmdbWorking = configCheck.apiTest("tmdb", configData['apiKeys'][0]['key'], debugMode)
			tvdbWorking = configCheck.apiTest("tvdb", configData['apiKeys'][1]['key'], debugMode)
			omdbWorking = configCheck.apiTest("omdb", configData['apiKeys'][2]['key'], debugMode)

			# Currently focusing on tmdb. Should consider how to add support for others later.
			#   Example: read config for preferred api-only or preferred order (might fail to find a title with one?)
			if tmdbWorking:
				# Produce a menu to the user if no file paths provided.
				if not filePaths:
					utilities.beginMenu()
							
				# Otherwise, begin making use of file paths.
				else:
					
					# Initialise some variables that we'll use later:

					validPaths, invalidPaths = [], []
					inputPathsProcessedCount = 0     				# Count used to track how many input directories (parametors) have been processed.
					processedFileCount = 0							# Same as above but for files.

					# Error lists

					cleanupPaths, renameErrors, renameArray = [],[],[]		# Lists for holding paths about errors, clean up errors, rename errors and the planned renames.

					# Run preliminary checks
					for currentPath in filePaths:
						try:
							validCheck = renamer.pathValid(currentPath)		# Run the validPath checker
							if validCheck[0]:
								validPaths.append(currentPath)				# Append to valid path list if accepted
							else:
								invalidPaths.append(currentPath)			# Append to invalid path list if not accepted

							
						except:
							print("\n-- Critical Error: Problem running preliminary checks on: "+currentPath)
							utilities.writeLine()
							raise
					
					

					# Once the preliminary checks are complete, move onto actual sorting.
									
					if debugMode:
						utilities.pathValidityDebug(validPaths, invalidPaths)	# Output validity listings if debug mode enabled	
						
					for path in validPaths:
						sortingResult = renamer.sorter(path, debugMode)
				
						if sortingResult[0] == False:
							print("\n-- Error: "+sortingResult[1])
							print("'"+currentPath+"'\n")
						else:
							inputPathsProcessedCount+=1					# Increment the processed path count.
							renameArray.append({'title':sortingResult[2], 'year':sortingResult[3]})

					utilities.writeLine()
					for a in renameArray:
						print(a['title'], "("+a['year']+")")

					
					#print(currentPath)
				
			
	
	# End of application
	print("\n-- Info: Application closure.\n")
	os.system("pause")

except Exception as e:
	#os.system("pause")
	print("Sorry, looks like the app has failed somewhere...\nPlease provide the following information to me on my github page:\n")
	os.system("pause")
	raise