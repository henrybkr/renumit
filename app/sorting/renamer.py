# -*- coding: utf-8 -*-

##########################################################################################################################
## This file contains functions that primarily deals with the renaming of files.										##
##########################################################################################################################

# Required imports
import sys
import os
#sys.path.insert(1, r'\app\scripts')
#sys.path.insert(1, r'\app\api')
#from Renumit.app.scripts import utilities, filenameReview # pylint: disable=import-error
from ..scripts import utilities
from ..sorting import filenameReview, modifyFile
import shutil
import time
from progress.bar import Bar
from app.api import tmdbHelper

# Run a handful of checks to confirm path is valid, otherwise report back the error.
def pathValid(inputPath):
	error = "No error"
	if not utilities.checkExist(inputPath):
		error = "Path provided does not exist"
		return (False, error)

	else:
		return (True, error)


# Parse the name and year from the original FILE itself.
def getNameYear(inputPath, debugMode):
	error = False
	# At this point, we are assuming the path exists.
	
	# Year collection
	yearResponse = filenameReview.getYear(inputPath, debugMode)

	year = False				# Default
	if yearResponse[0]:
		year = yearResponse[0]
	else:
		print("-- Error: "+yearResponse[1])

	# Title collection with or without year
	if year:
		title = filenameReview.getName(inputPath, debugMode, year)
	else:
		title = filenameReview.getName(inputPath, debugMode)

	return (True, error, title, year)

# Function to get output filenames and directory names based on the user config and details we have at hand
def getNames(configJSON, nameYearList, filenameData, mediaInfoData):
	
	space = configJSON['spaceCharacter']																					# Collect the character the user prefers to use as a 'space' character.

	response = tmdbHelper.search(configJSON['apiKeys'][0]['key'], nameYearList['title'], nameYearList['year'])				# First run a search via TMDB api

	#localTitle				= utilities.addSpaces(nameYearList['title'],space)												# Collect name and year from the local file.	
	#localYear				= utilities.addSpaces(nameYearList['year'],space)
	localNameYear		= nameYearList['title']+" ("+nameYearList['year']+")"

	## Now run the comparison function to looks for an appropriate match the search data

	try:
		parsedResponse = tmdbHelper.compareTMDBNameYear(response, localNameYear, configJSON)															
		#utilities.printColor("orange", parsedResponse, always=True)
		if parsedResponse:
			title = utilities.addSpaces(parsedResponse['title'],space)
			year = parsedResponse['year']
			yearBrackets = utilities.addSpaces("("+year+")", space)
		else:
			return False																									## No results found. Skip?
	except:
		utilities.printColor("red", "parseTMDB error", always=True)
		raise

	resolution			= utilities.addSpaces((str(mediaInfoData['height'])+mediaInfoData['scanType']),space)
	codec				= utilities.addSpaces(mediaInfoData['codec'],space)
	edition				= utilities.addSpaces(filenameData['edition'],space)
	source				= utilities.addSpaces(filenameData['source'],space)
	ext					= filenameData['extension']

	newOutputFilename = (title+yearBrackets+resolution+codec+edition+source).strip()+ext
	
	if space == ".":
		newDirName = title+space+nameYearList['year']
	else:
		newDirName = nameYearList['title']+" ("+nameYearList['year']+")"

	return {'directory': newDirName, 'filename': newOutputFilename}

def getNewExtraPath(configJSON, debugMode, currentFullPath, confirmedNewFilename):
	folder = configJSON['bonusFolderName']

	path = currentFullPath.lower()
	#print(path)

	if ("\\deleted scenes\\" in path):
		newFolderPath = "\\"+folder+"\\Deleted Scenes\\"
	elif ("\\interviews\\" in path):
		newFolderPath = "\\"+folder+"\\Interviews\\"
	elif ("\\trailers\\" in path):
		newFolderPath = "\\"+folder+"\\Trailers\\"
	elif ("\\behind the scenes\\" in path):
		newFolderPath = "\\"+folder+"\\Behind The Scenes\\"
	elif ("\\featurettes\\" in path) or ("\\extra\\" in path) or ("\\extras\\" in path) or ("\\bonus\\" in path):

		#if "mkv" in path:				# Skip if not a mkv file
		
		if "main menu" in path:
			newFolderPath = "\\"+folder+"\\"
		elif "menu" in path:
			newFolderPath = "\\"+folder+"\\"
		elif "trailer" in path:
			newFolderPath = "\\"+folder+"\\Trailers\\"
		elif "promo.mkv" in path:
			newFolderPath = "\\"+folder+"\\"
		elif "deleted" in path and "scene" in path:
			newFolderPath = "\\"+folder+"\\Deleted Scenes\\"
		elif "interview" in path:
			newFolderPath = "\\"+folder+"\\Interviews\\"
		elif "short" in path:
			newFolderPath = "\\"+folder+"\\Shorts\\"
		elif "extra.mkv" in path or "extras.mkv" in path:
			newFolderPath = "\\"+folder+"\\"
		elif ".m4a" in path or ".mp3" in path or ".wav" in path or ".flac" in path:
			newFolderPath = "\\"+folder+"\\Soundtrack\\"
		else:
			newFolderPath = "\\"+folder+"\\"

	else:
		#if "mkv" in path:				# Skip if not a mkv file

		if "main menu" in path:
			newFolderPath = "\\"+folder+"\\"
		elif "menu" in path:
			newFolderPath = "\\"+folder+"\\"
		elif "trailer" in path:
			newFolderPath = "\\"+folder+"\\"
		elif "promo.mkv" in path:
			newFolderPath = "\\"+folder+"\\"
		elif "extra.mkv" in path or "extras.mkv" in path:
			newFolderPath = "\\"+folder+"\\"
		elif debugMode:
			if utilities.confirm("Having trouble with a file. Is '"+path+"' an extra?"):
				newFolderPath = "\\Featurettes\\"
			else:
				skip = True
		else:
			newFolderPath = "\\Featurettes\\"	# Assume file is a bonus file

	#utilities.printColor("yellow", newFolderPath, always=True)
	return newFolderPath+confirmedNewFilename

# Function to check and potentially modify input filenames
def checkFilename(configJSON, inputFilename):

	## Here we should run a few things:

	# - Checks for bad characters (non-english characters that might mess with a media database)
	# - Remove keywords that the user has defined
	# - etc

	# Note, don't try to do everything here. Launch other functions here as each might get larger.

	outputFilename = removePrefKeywords(configJSON, inputFilename)

	return outputFilename

def removePrefKeywords(configJSON, inputFilename):
	
	##

	return inputFilename

# Class for a custom progress bar based on the default one.
class CustomBar(Bar):
	fill = '*'
	suffix = '%(percent).1f%% - %(eta)ds'
	empty_fill = '∙'
	fill = utilities.getColor('orange','█')

# Function that runs the move function but also keeps note of overall progress.
def moveElements(renames, configData):
	debugMode = True
	bar = CustomBar("Processing files", max=len(renames))			# A progress bar, the max set to the length of the list
	issues = []
	
	with bar:
		for r in renames:

			## Note to self, need work here... Detect non-video files and determine if we should rename them, delete them or just skip over them. ref: deleteOrIgnore function.


			"""
			if not "mkv" in r[0] or not "mp4" in r[0]:
				# First check if we ignore or delete non-video files.									
				response = utilities.deleteOrIgnore(configData, debugMode, r[0])					# Run the function to decide what to do with the non-video filetype, depending on user settings.
				print(response)


				if response['issue'] == True:
					print(response['message'])
				
				elif response['shouldRename']:
					## Should skip renaming
					response = move(r, configData)									# Run the rename function with the current list elements, keep note of the response.

			else:
				response = move(r, configData)									# Run the rename function with the current list elements, keep note of the response.
			"""
			response = move(r, configData)									# Run the rename function with the current list elements, keep note of the response.

			if not bool(response['response']):
				issues.append([r,response['error']])
			
			bar.next()

	if issues:
		utilities.printColor("yellow", "\n-- Warning: Processing of files complete With these errors:\n", always=True)
		
		utilities.failedMoveTable(issues)
		#for x in issues:
		#	utilities.printColor("red", x, always=True)
	else:
		utilities.printColor("green", "\n-- Info: Processing of files completed with no errors.\n", always=True)

def makeDirForFile(inputFilename):
	os.makedirs(os.path.dirname(inputFilename))				# Create content directory

def move(arrayElement, configFile):
	response = False
	error = ""
	mkvModifierConfig = [False, False]

	# Check that the config answers are valid, else return errors and fail next step.
	try:
		shouldDeleteCovers = int(configFile['removeCovers'])
	except:
		print("Failed to get config file['removeCovers']")
		shouldDeleteCovers = 0
	try:
		shouldRemoveMKVTitle = int(configFile['removeMKVTitle'])
	except:
		print("Failed to get config file['removeCovers']")
		shouldRemoveMKVTitle = 0

	if shouldRemoveMKVTitle and shouldDeleteCovers:
	
		if not utilities.checkExist(arrayElement[1]):
			# Create the directory required for this file if not already present.
			if not utilities.checkExist(os.path.dirname(arrayElement[1])):		# If folder doesn't already exist
				makeDirForFile(arrayElement[1])

			if ".mkv" in arrayElement[0]:																													# Additional check to make sure file is a .mkv file.
				if not (arrayElement[2]):																													# File is a 'extra' file.
					# Check if we should remove covers...
					if shouldDeleteCovers == 2 or shouldDeleteCovers == 1:
						#utilities.printColor("red", "EXTRA --- should delete cover for: "+arrayElement[1], always=True)
						mkvModifierConfig[0] = True																												# Set the remove cover flag for this file - used later.
					# Then check if we should remove title from video track on the mkv
					if shouldRemoveMKVTitle == 2 or shouldRemoveMKVTitle == 1:
						#utilities.printColor("purple", "EXTRA --- should delete title for: "+arrayElement[1], always=True)
						mkvModifierConfig[1] = True																												# Set the remove title flag for this file - used later.
					
				else:																																		# File is a 'main' movie file.
					# Check if we should remove covers...
					if shouldDeleteCovers == 1:
						#utilities.printColor("cyan", "MAIN --- should delete cover for: "+arrayElement[1], always=True)
						mkvModifierConfig[0] = True					# Set the remove cover flag for this file - used later.
					# Then check if we should remove title from video track on the mkv
					if shouldRemoveMKVTitle == 1:
						#utilities.printColor("purple", "MAIN --- should delete title for: "+arrayElement[1], always=True)
						mkvModifierConfig[1] = True																												# Set the remove title flag for this file - used later.


				#utilities.printColor("green", "launch the mkv patch function?", always=True)
				if mkvModifierConfig[0] or mkvModifierConfig[1]:
					modifyFile.updateTracks(arrayElement[0], mkvModifierConfig)							# Launch MKV track edit function, passing config settings.


				response = False																		# Default response. Suggests failure unless confirmed otherwise.
				shutil.move(arrayElement[0], arrayElement[1])											# Move the content to destination directory with new filename
				if utilities.checkExist(arrayElement[1]):												# Confirm the newly moved file now exists
					if not utilities.checkExist(arrayElement[0]):										# Confirm the old file location is now gone
						response = True																	# Set response to true when all conditions are met
					else:
						error = "Move attempted - The newly moved file exists but it still exists in the old location."
				else:
					error = "Move attempted - Moved file doesn't exist. Potential permission error."
			else:
				error = "This file is not a mkv file and was skipped."
		else:
			error = "File already exists."
	else:
		error = "Failed a check regarding MKV title and cover. Please check your config file."

	return {'response': response, 'error': error}													# Return a response and any error we might have come across
	
	

