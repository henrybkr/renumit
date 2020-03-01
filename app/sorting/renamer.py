# -*- coding: utf-8 -*-

##########################################################################################################################
## This file contains functions that primarily deals with the renaming of files.										##
##########################################################################################################################

# Required imports
import sys
sys.path.insert(1, r'\app\scripts')
sys.path.insert(1, r'\app\api')
import utilities, filenameReview # pylint: disable=import-error
import shutil
import time
from progress.bar import Bar

# Run a handful of checks to confirm path is valid, otherwise report back the error.
def pathValid(inputPath):
	error = "No error"
	if not utilities.checkExist(inputPath):
		error = "Path provided does not exist"
		return (False, error)

	else:
		return (True, error)

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
	
	"""
	# Debug output only
	if debugMode:
		print("\nDebug Output: ")
		utilities.writeLine()
		print('Input Path -- '+inputPath)
		try:
			print('Movie Title & Year -- '+title+' ('+year+')')
		except:
			print('Movie Title -- '+title+' -- no valid year found')
	"""

	return (True, error, title, year)


# Function to get output filenames and directory names based on the user config and details we have at hand
def getNames(configJSON, nameYearList, filenameData, mediaInfoData):
	
	space = configJSON['spaceCharacter']

	#newDir = nameYearList['title']+space+"("+str(nameYearList['year'])+")"	
	
	title		= utilities.addSpaces(nameYearList['title'],space)
	year		= utilities.addSpaces(nameYearList['year'],space)
	year_brackets		= utilities.addSpaces(("("+nameYearList['year']+")"),space)

	resolution	= utilities.addSpaces((str(mediaInfoData['height'])+mediaInfoData['scanType']),space)
	codec		= utilities.addSpaces(mediaInfoData['codec'],space)
	edition		= utilities.addSpaces(filenameData['edition'],space)
	source		= utilities.addSpaces(filenameData['source'],space)
	ext			= filenameData['extension']

	newOutputFilename = (title+year_brackets+resolution+codec+edition+source).strip()+ext
	
	if space == ".":
		newDirName = title+space+nameYearList['year']
	else:
		newDirName = nameYearList['title']+" ("+nameYearList['year']+")"

	return {'directory': newDirName, 'filename': newOutputFilename}

def getNewExtraPath(configJSON, debugMode, currentFullPath, confirmedNewFilename):
	folder = configJSON['bonusFolderName']

	path = currentFullPath.lower()


	if ("\\deleted scenes\\" in path):
		newFolderPath = "\\"+folder+"\\Deleted Scenes\\"
	elif ("\\interviews\\" in path):
		newFolderPath = "\\"+folder+"\\Interviews\\"
	elif ("\\trailers\\" in path):
		newFolderPath = "\\"+folder+"\\Trailers\\"
	elif ("\\behind the scenes\\" in path):
		newFolderPath = "\\"+folder+"\\Behind The Scenes\\"
	elif ("\\featurettes\\" in path) or ("\\extra\\" in path) or ("\\extras\\" in path) or ("\\bonus\\" in path):
		newFolderPath = "\\"+folder+"\\"
	else:
		if "mkv" in path:				# Skip if not a mkv file
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
				newFolderPath = "\\Featurettes\\"	# Assume file is a featurette

	
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
def moveElements(renames):
	bar = CustomBar("Processing files", max=len(renames))			# A progress bar, the max set to the length of the list
	issues = []
	
	with bar:
		for r in renames:

			response = move(r)									# Run the rename function with the current list elements, keep note of the response.

			if not bool(response['response']):
				issues.append([r,response['error']])
			bar.next()
	utilities.printColor("yellow", "\nProcessing of files complete.\n", debugMode=True)

	if issues:
		for x in issues:
			print(x)

def move(arrayElement):
	response = False
	error = ""

	#print(arrayElement[0]+" ---> "+arrayElement[1])

	if not utilities.checkExist(arrayElement[1]):
		utilities.printColor("yellow", "Attempting to move...")
		#shutil.move(arrayElement[0], arrayElement[1])											# Move the content to destination directory with new filename
		if utilities.checkExist(arrayElement[1]):												# Confirm the newly moved file now exists
			if utilities.checkExist(arrayElement[0]):											# Confirm the old file location is now gone
				response = True																	# Set response to true when all conditions are met
			else:
				error = "Move attempted - The newly moved file exists but it still exists in the old location."
		else:
			error = "Move attempted - The newly moved file doesn't exist."
	else:
		error = "File already exists."
	
	return {'response': response, 'error': error}

