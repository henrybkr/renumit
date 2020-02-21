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

	# elif something?
	# Other checks, such as characters used are acceptable.
	##
	##

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


# Function to get an output directory based on the user config and details we have at hand
def getNewFilename(configJSON, nameYearList, filenameData, mediaInfoData):

	newOutputFilename = nameYearList['title']+" ("+nameYearList['year']+") "+str(mediaInfoData['height'])+mediaInfoData['scanType']+" "+mediaInfoData['codec']+" "+filenameData['source']

	return newOutputFilename

def getNewDirName(configJSON, nameYearList, filenameData, mediaInfoData):

	newDirName = nameYearList['title']+" ("+nameYearList['year']+")"

	return newDirName