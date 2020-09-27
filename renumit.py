# -*- coding: utf-8 -*-

##########################################################################################################################
## ~ A Python script used for querying databases and renaming media accordingly based on personal preference and        ##
##   support for the Plex media servers.                                                                                ##
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

from app.scripts import utilities
from app.scripts import configCheck
from app.scripts import readConfig
from app.sorting import filenameReview, mediaInfoReview, renamer

#########################
# Global variables, testing only:
testMode = True

#########################
# Application run order:

try:
	mainDir = os.path.dirname(os.path.abspath(__file__))
	#print(mainDir)
	#os.system("pause")

	utilities.clear_win()																														# Clear the window on first launch.

	utilities.intro(mainDir)																													# Run application intro.
	

	apiKeychain = []
	debugMode = False																															# Set to false but later overwritten.

	configJSON = readConfig.read(mainDir)																										# Collect config json.
	configData = json.loads(configJSON)

	if not(configJSON):
		print("-- Hmm, problem with your configuration settings!")
	else:
		debugMode = bool(configData['debugMode'])																								# Enable debug flag if in config data.
		utilities.writeLine()
		utilities.printColor("green", "-- Config file loaded ----------------------------------------------------------------------------", debugMode=debugMode)
		
		apiCheckResult = configCheck.apiKeyAvailable(configData['apiKeys'])																		# Confirm api keys work.
		
		if not apiCheckResult[0]:
			utilities.printColor("red", "\n-- Critical Error: No API keys available. Please add at least one to preferences.config.", always=True)
		else:
			# If at least one api key is found, test which ones are working.
			if apiCheckResult[0] == 2:
				utilities.printColor("green", apiCheckResult[1], debugMode=debugMode)																										# Output api key info.
			else:
				utilities.printColor("yellow", apiCheckResult[1], debugMode=debugMode)																										# Output api key info.

			# Now lets check that the keys are functional.
			tmdbWorking = configCheck.apiTest("tmdb", configData['apiKeys'][0]['key'], debugMode)
			tvdbWorking = configCheck.apiTest("tvdb", configData['apiKeys'][1]['key'], debugMode)
			omdbWorking = configCheck.apiTest("omdb", configData['apiKeys'][2]['key'], debugMode)

			# Currently focusing on tmdb. Should consider how to add support for others later.
			#   Example: read config for preferred api-only or preferred order (might fail to find a title with one?)

			filePaths = utilities.getValidPaths(debugMode, sys.argv[1:])																		# Review potential file paths provided to app. Return valid paths.
			# Produce a menu to the user if no file paths provided.

			if not sys.argv[1:]:
				utilities.beginMenu()
			elif filePaths:
			
				## Start with TMDB
				if tmdbWorking:	
					
					# Initialise some variables that we'll use later:
					validPaths, invalidPaths = [], []
					inputPathsProcessedCount = 0     				# Count used to track how many input directories (parametors) have been processed.
					processedFileCount = 0							# Same as above but for files.
					if not configData['relativeRename']:
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
					
					# Once the preliminary checks are complete, move onto grabbing info				
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
					
					

					temp_pathMainContentList = []								# Empty list to be used to store potential "main" files (movie).
					pathMainContentList = []

					i = 0													# Used for getting the name and year from array.
					
					bar = renamer.CustomBar("Preparing Renames", max=len(validPaths))			# A progress bar, the max set to the length of the list
					with bar: 
						for path in validPaths:

							# First we need to confirm if we need a relative output directory or not.

							if configData['relativeRename']:
								sortedDir = utilities.getRelativeOutputPath(path, configData['sortedDirectory'])

								if not utilities.checkExist(sortedDir):
									if not utilities.forceMakeDir(sortedDir):
										raise Exception("Problem making relative directory. Please report the issue!")
							
							# Now move onto reviewing files.

							mainMovieFileLocated = False

							# First check if the provided path itself has a container (.mkv)
							if os.path.isfile(path):
								
								# confirm if path is a mkv/mp4 file
								if ".mkv" in path or ".mp4" in path:
									mainMovieFileLocated = True
									temp_pathMainContentList = [path]
								else:
									sortingErrors.append({'path': path, 'error': "Bad file. Appears to be a non-media file."})	# Report back and error about multiple video files in main movie directory.
								
							# If the path is a directory
							elif (os.path.isdir(path)):
								myPath = re.sub(r'([\[\]])','[\\1]',path)														# Note to self, glob doesn't seem to like square brackets, so removing seems to do the trick
								temp_pathMainContentList = [f for f in glob.glob(myPath + "**/*.*", recursive=True)]					# Collect a full list of all files in the main directory
								
								# In the event of more than one "main" file being located...
								if len(temp_pathMainContentList) > 1:

									for x in temp_pathMainContentList:
										
										if not (".mkv" in x or ".mp4" in x):										
											utilities.deleteOrIgnore(configData, debugMode, x)									# Run the function to decide what to do with the non-video filetype, depending on user settings.
										else:
											pathMainContentList.append(x)														# Remove non video files from the array if any exist.

									#for j in pathMainContentList:
									#	utilities.printColor("yellow", j, always=True)

									pathMainContentList = temp_pathMainContentList
									
									# Check to see if still more than one video file remains in the list
									if len(pathMainContentList) != 1:
										#print("updated list = ")
										#print(pathMainContentList)
										sortingErrors.append({'path': path, 'error': "More than one file in main directory"})	# Report back and error about multiple video files in main movie directory.
									else:
										#if debugMode:
											#print(("Debug -- Confirmed updated 'main' file: ")+utilities.getColor("yellow", pathMainContentList[0]))
										mainMovieFileLocated = True
								elif len(temp_pathMainContentList) == 0:
									sortingErrors.append({'path': path, 'error': "No main file found. Potential empty folder"})	# Report back issue with finding the "main" media file.
								
								else:
									pathMainContentList = temp_pathMainContentList
									# Only one "main" file found in the directory (good!)
									mainMovieFileLocated = True

							# Error handling, output error.
							else:
								print("Warning -- Issue detecting if path is a file or a directory.")
						
							
							# Will only continue if the main movie file is located.
							if mainMovieFileLocated:
								try:
									if os.path.isfile(path):
										mainMovieFile = path
									else:
										mainMovieFile = pathMainContentList[0]
								except:
									utilities.printColor("yellow", "\n-- Warning: Issue selecting main content file.", always=True)
									raise
								
								# Only continue if main content is located.
								if mainMovieFile:
									# Now begin to collect information about this full file path and create new names
									
									filenameData = filenameReview.reviewPath(mainMovieFile)															# Run script to determine information about the path. Requires relative path for splitting.
									mediaInfoData = mediaInfoReview.basicInfo(mainMovieFile)

									newNames = renamer.getNames(configData, nameYearsArray[i], filenameData, mediaInfoData)							# Get folder and file names for the sort
									if not newNames:
										sortingErrors.append({'path': path, 'error': "Couldn't find an appropriate TMDB entry for this release"})

									else:
										renameArray.append([mainMovieFile, (sortedDir+"\\"+newNames['directory']+"\\"+newNames['filename']), True])		# Append the original main file location and the new location. Set third array column as true to highlight is main file.

										# Now turn to additional files inside the directory. Collect all files listings and remove the "main" file
										extraFiles = []																									# Empty list to hold all full file listings from the input path
										for (current_path, dirs, files) in os.walk(validPaths[i]):
											for file in files:
												ext = os.path.splitext(file)[1]
												full_path = (current_path+"\\"+file)
												extraFiles.append(full_path)								

										if len(extraFiles) > 0:

											extraFiles.remove(mainMovieFile)															# Remove the "main" file from the full list of all files

											# Now get new filenames for any bonus files that we plan to keep
											for y in extraFiles:
												onlyFile = os.path.basename(y)
												confirmedFilename = renamer.checkFilename(configData, onlyFile)
												renameArray.append([y, (sortedDir+"\\"+newNames['directory']+renamer.getNewExtraPath(configData, debugMode, y, confirmedFilename, path)), False])
						
							bar.next()
							i+=1																								# Finish this loop by incrementing the reference number variable 

					utilities.renameTable(renameArray, debugMode)																# Output the expected renames if in debug mode (table format)

					# Launch the error report functionality. Only displays errors if there are any.
					utilities.reportErrors(filePaths, invalidPaths, sortingErrors)

					# Only continue at this point if there is confirmed renames to process.
					if(len(renameArray) <= 0):
						utilities.printColor("yellow", "\n-- Warning: Cannot continue as there are no valid renames to process.", always=True)
					else:
						# Output some user config settings if in debug mode:
						if debugMode:
							utilities.configTable(configData)

						

						if utilities.confirm("Ready to rename?"):
							utilities.writeLine()

							#response = renamer.moveElements(renameArray)
							
							renamer.moveElements(renameArray, configData)

							for pathToClean in filePaths:
								utilities.deleteEmptyDirs(pathToClean)
							
							## Note to self, probably need some kind of check for the response. If true, add error to an array. Once all moves have been completed, output green success for all okay, yellow for some errors, red for all errors.

							#utilities.printColor("green", "move function complete", debugMode=True)

			else:
				utilities.printColor("yellow", "\n-- Warning: Looks like there are no valid paths to rename.", always=True)
			
			
	
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