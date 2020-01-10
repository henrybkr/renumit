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
import re
import glob

#########################
# Internal imports
#########################
# Include other path locations at runtime for easier access to package files, etc in different directories

sys.path.insert(1, r'app\api')
sys.path.insert(1, r'app\history')
sys.path.insert(1, r'app\scripts')
sys.path.insert(1, r'app\sorting')

import utilities, readConfig, configCheck, filenameReview, renamer, tmdbHelper # pylint: disable=import-error

#########################
# Global variables, testing only:
testMode = True

#########################
# Application run order:
try:
	utilities.clear_win()																										# Clear the window on first launch.
	filePaths = utilities.intro(sys.argv[1:])																					# Run intro and review potential file paths provided to app
	
	mainDir = os.path.dirname(os.path.abspath(__file__))
	configJSON = readConfig.read(mainDir)													# Collect config json.
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

					cleanupPaths, renameErrors, nameYearsArray, renameArray = [],[],[],[]		# Lists for holding paths about errors, clean up errors, rename errors and the planned renames.

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
					
					# Output validity listings if debug mode enabled
					if debugMode:
						utilities.pathValidityDebug(validPaths, invalidPaths)
					
					# Once the preliminary checks are complete, move onto actual sorting						
					for path in validPaths:
						sortingResult = renamer.sorter(path, debugMode)
				
						if sortingResult[0] == False:
							print("\n-- Error: "+sortingResult[1])
							print("'"+currentPath+"'\n")
						else:
							inputPathsProcessedCount+=1						# Increment the processed path count.
							nameYearsArray.append({
								'title':sortingResult[2],
								'year':sortingResult[3]
								})

					utilities.nameYearTable(nameYearsArray)					# Output list of expected valid name/years we'll be processing
					
					utilities.writeLine()

					for path in validPaths:
						mainMovieFileLocated = False
						myPath = re.sub(r'([\[\]])','[\\1]',path)														# Note to self, glob doesn't seem to like square brackets, so removing seems to do the trick
						pathMainContentList = [f for f in glob.glob(myPath + "**/*.*", recursive=True)]					# Collect a full list of all files in the main directory
						
						# In the event of more than one "main" file being located...
						if len(pathMainContentList) > 1:
							for x in pathMainContentList:
								if not ".mkv" in x or not ".mp4" in x:
									pathMainContentList.remove(x)														# Remove non video files from the array if any exist.

							# Check to see if still more than one video file remains in the list
							if not len(pathMainContentList) > 1:
								renameErrors.append({'path': path, 'error': "More than one file in main directory"})	# Report back and error about multiple video files in main movie directory.
							else:
								mainMovieFileLocated = True
						elif len(pathMainContentList) == 0:
							renameErrors.append({'path': path, 'error': "No main file found. Potential empty folder"})	# Report back issue with finding the "main" media file.
						
						else:
							# Only one "main" file found in the directory (good!)
							mainMovieFileLocated = True
					
						# Will only continue if the main movie file is located.
						if mainMovieFileLocated:
							try:
								mainMovieFile = pathMainContentList[0]
							except:
								print("Warning -- Issue selecting main content file")
							
							# Only continue if main content is located.
							if mainMovieFile:
								# Now begin to collect information about this full file path.
								
								renameData = filenameReview.reviewPath(mainMovieFile)						# Run script to determine information about the path. Requires relative path for splitting.
								print(renameData)



					# Launch the error report functionality. Only displays errors if there are any.
					utilities.reportErrors(filePaths, invalidPaths, renameErrors)
				
			
	
	# End of application
	print("\n-- Info: Application closure.\n")
	os.system("pause")

except Exception as e:
	#os.system("pause")
	print("\n\n"+utilities.line+"\nSorry, looks like the app has failed somewhere...\nPlease provide the following information to me on my github page:\n"+utilities.line+"\nhttps://github.com/henrybkr/renumit\n"+utilities.line)
	
	# Raise the issue only if the internal debug mode active.
	if testMode:
		raise
	os.system("pause")