# -*- coding: utf-8 -*-

##########################################################################################################################
## ~ A Python script used for querying databases and renaming media accordingly based on personal preference and        ##
##   support for the Plex media servers.                                                                                ##
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

import utilities, readConfig, configCheck, filenameReview, renamer, tmdbHelper, mediaInfoReview # pylint: disable=import-error

#########################
# Global variables, testing only:
testMode = True

#########################
# Application run order:
try:
	utilities.clear_win()																										# Clear the window on first launch.
	filePaths = utilities.intro(sys.argv[1:])																					# Run intro and review potential file paths provided to app.
	
	mainDir = os.path.dirname(os.path.abspath(__file__))
	configJSON = readConfig.read(mainDir)																						# Collect config json.
	configData = json.loads(configJSON)
	apiKeychain = []
	debugMode = False																											# Set to false but later overwritten.

	if not(configJSON):
		print("-- Hmm, problem with your configuration settings!")
	else:
		utilities.writeLine()
		print("-- Config file loaded ----------------------------------------------------------")
		
		apiCheckResult = configCheck.apiKeyAvailable(configData['apiKeys'])														# Confirm api keys work.
															
		debugMode = bool(configData['debugMode'])																				# Enable debug flag if in config data.
		
		
		if not apiCheckResult[0]:
			print("\n-- Critical Error: No API keys available. Please add at least one to preferences.config.")
		else:
			# If at least one api key is found, test which ones are working.
			if debugMode:
				print(apiCheckResult[1])																						# Output api key info.

			# Now lets check that the keys are functional.
			tmdbWorking = configCheck.apiTest("tmdb", configData['apiKeys'][0]['key'], debugMode)
			tvdbWorking = configCheck.apiTest("tvdb", configData['apiKeys'][1]['key'], debugMode)
			omdbWorking = configCheck.apiTest("omdb", configData['apiKeys'][2]['key'], debugMode)

			


				

			# Currently focusing on tmdb. Should consider how to add support for others later.
			#   Example: read config for preferred api-only or preferred order (might fail to find a title with one?)
			
			# Produce a menu to the user if no file paths provided.
			if not filePaths:
				utilities.beginMenu()
			else:
			
				## Start with TMDB
				if tmdbWorking:	
					
					# Initialise some variables that we'll use later:
					validPaths, invalidPaths = [], []
					inputPathsProcessedCount = 0     				# Count used to track how many input directories (parametors) have been processed.
					processedFileCount = 0							# Same as above but for files.
					sortedDir = configData['sortedDirectory']

					# Error lists
					cleanupPaths, sortingErrors, nameYearsArray, renameArray = [],[],[],[]		# Lists for holding paths about errors, clean up errors, rename errors and the planned renames.

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
						getNameYear_result = renamer.getNameYear(path, debugMode)
				
						if getNameYear_result[0] == False:
							print("\n-- Error: "+getNameYear_result[1])
							print("'"+currentPath+"'\n")
						else:
							inputPathsProcessedCount+=1						# Increment the processed path count.
							nameYearsArray.append({
								'title':getNameYear_result[2],
								'year':getNameYear_result[3]
								})

					utilities.nameYearTable(nameYearsArray)					# Output list of expected valid name/years we'll be processing.
					
					utilities.writeLine()

					pathMainContentList = []								# Empty list to be used to store potential "main" files (movie).

					i = 0													# Used for getting the name and year from array. 
					for path in validPaths:
						mainMovieFileLocated = False

						# First check if the provided path itself has a container (.mkv)
						if os.path.isfile(path):
							# confirm if path is a mkv/mp4 file
							if ".mkv" in path or not ".mp4" in path:
								mainMovieFileLocated = True
								pathMainContentList.append(path)
							else:
								sortingErrors.append({'path': path, 'error': "Bad file. Appears to be a non-media file."})	# Report back and error about multiple video files in main movie directory.
							
						# If the path is a directory
						elif (os.path.isdir(path)):
							myPath = re.sub(r'([\[\]])','[\\1]',path)														# Note to self, glob doesn't seem to like square brackets, so removing seems to do the trick
							pathMainContentList = [f for f in glob.glob(myPath + "**/*.*", recursive=True)]					# Collect a full list of all files in the main directory
							# In the event of more than one "main" file being located...
							if len(pathMainContentList) > 1:

								for x in pathMainContentList:
									
									if not (".mkv" in x or ".mp4" in x):										
										utilities.deleteOrIgnore(configData, debugMode, x)									# Run the function to decide what to do with the non-video filetype, depending on user settings.
										pathMainContentList.remove(x)														# Remove non video files from the array if any exist.

								# Check to see if still more than one video file remains in the list
								if len(pathMainContentList) != 1:
									print("updated list = ")
									print(pathMainContentList)
									sortingErrors.append({'path': path, 'error': "More than one file in main directory"})	# Report back and error about multiple video files in main movie directory.
								else:
									if debugMode:
										print("Located a single 'main' file")
									mainMovieFileLocated = True
							elif len(pathMainContentList) == 0:
								sortingErrors.append({'path': path, 'error': "No main file found. Potential empty folder"})	# Report back issue with finding the "main" media file.
							
							else:
								# Only one "main" file found in the directory (good!)
								mainMovieFileLocated = True
						# Error handling, output error.
						else:
							print("Warning -- Issue detecting if path is a file or a directory.")
					
						# Will only continue if the main movie file is located.
						if not mainMovieFileLocated:
							print("Warning -- Looks like we can't find a main file for this path. Needs debugging.")
						else:
							try:
								mainMovieFile = pathMainContentList[0]
							except:
								print("Warning -- Issue selecting main content file")
							
							# Only continue if main content is located.
							if mainMovieFile:
								# Now begin to collect information about this full file path and create new names
								
								filenameData = filenameReview.reviewPath(mainMovieFile)										# Run script to determine information about the path. Requires relative path for splitting.
								mediaInfoData = mediaInfoReview.basicInfo(mainMovieFile)

								newNames = renamer.getNames(configData,nameYearsArray[i],filenameData, mediaInfoData)		# Get folder and file names for the sort
								
								renameArray.append([mainMovieFile, (sortedDir+r"/"+newNames['directory']+r"/"+newNames['filename']), True])
								
								#print(newNames['directory']+r"/"+newNames['filename'])

								# Now turn to additional files inside the directory. Collect all files listings and remove the "main" file

								extraFiles = []																				# Empty list to hold all full file listings from the input path
								for (current_path, dirs, files) in os.walk(validPaths[i]):
									for file in files:
										ext = os.path.splitext(file)[1]
										#filename = os.path.splitext(file)[0].replace("."," ")
										full_path = (current_path+"\\"+file)
										extraFiles.append(full_path)
								

								extraFiles.remove(mainMovieFile)															# Remove the "main" file from the full list of all files
								#print(extraFiles)

								if len(extraFiles) > 0:

									# First check if we ignore or delete non-video files.

									for y in extraFiles:
										if not (".mkv" in y or ".mp4" in y):										
											utilities.deleteOrIgnore(configData, debugMode, y)								# Run the function to decide what to do with the non-video filetype, depending on user settings.
											extraFiles.remove(y)															# Remove non video files from the array if any exist.

									# Now get new filenames for any bonus files that we plan to keep

									for y in extraFiles:
										onlyFile = os.path.basename(y)
										confirmedFilename = renamer.checkFilename(configData, onlyFile)
										#blah = os.path.splitext(y)[0]
										#print(blah)
										renameArray.append([y, (sortedDir+"\\"+newNames['directory']+"\\"+newNames['filename']+renamer.getNewExtraPath(configData, debugMode, y, confirmedFilename)), False])

								
								#tempFiles.remove(mainMovieFile)

								#print(tempFiles)

						i+=1																								# Finish this loop by incrementing the reference number variable 
						
						utilities.writeLine()
						print("Okay, let's have a look at the mess:")
						utilities.writeLine()
						for z in renameArray:
							print(z[0]+" ---> "+z[1])



					# Launch the error report functionality. Only displays errors if there are any.
					utilities.reportErrors(filePaths, invalidPaths, sortingErrors)
			
			
	
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