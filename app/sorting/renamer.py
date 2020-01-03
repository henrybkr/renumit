# -*- coding: utf-8 -*-

##########################################################################################################################
## This file contains functions that primarily deals with the renaming of files.										##
##########################################################################################################################

# Required imports
import sys
sys.path.insert(1, r'\app\scripts')
sys.path.insert(1, r'\app\api')
import utilities, filenameReview # pylint: disable=import-error

def sorter(inputPath, debugMode):
	error = False
	
	# First check that the path is valid, otherwise fail (skipping this path)
	if not utilities.checkExist(inputPath):
		error = "Path provided does not exist"
		return (False, error, 0, 0)
	
	# If the path exists, continue with process
	else:
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

		print(inputPath)
		try:
			print('Movie Title -- '+title+' ('+year+')')
		except:
			print('Movie Title -- '+title+' -- no valid year found')
		#print(year)

		return (True, error, title, year)
