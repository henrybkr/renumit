# -*- coding: utf-8 -*-

##########################################################################################################################
## This file contains functions that primarily deals with the renaming of files.										##
##########################################################################################################################

# Required imports
import sys
sys.path.insert(1, r'\app\scripts')
sys.path.insert(1, r'\app\api')
import utilities, filenameReview # pylint: disable=import-error

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
	
	# Debug output only
	if debugMode:
		print("\nDebug Output: ")
		utilities.writeLine()
		print('Input Path -- '+inputPath)
		try:
			print('Movie Title & Year -- '+title+' ('+year+')')
		except:
			print('Movie Title -- '+title+' -- no valid year found')

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

	newOutputFilename = (title+year_brackets+resolution+codec+edition+source).strip()
	
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

	return inputFilename;