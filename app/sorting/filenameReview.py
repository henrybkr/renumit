# -*- coding: utf-8 -*-

##########################################################################################################################
## Primary use of this python file is to make assumptions based on the given file and folder name provided to it. Has	##
## 	the job of returning information such as edition among other things.												##
##########################################################################################################################

# Required imports
import sys
import re
sys.path.insert(1, r'\app\scripts')
sys.path.insert(1, r'\app\api')
import utilities # pylint: disable=import-error
from datetime import date

# Attempt to collect a name and year from a path
def getYear(path, debug):
	
	# Notes -- Make attempts to collect the year from the path string. Can sometimes give false results, thus multiple tries.
	# First looks for single 4 digits in brackets "(2000)"
	# Then looks for square brackets "[2000]"
	# Then looks for 4 digits surrounded by whitespace on each side " 2000 ". Dot titles are converted to spaces so bypasses that issue.
	# Fail if still not found.

	filename = path.replace(".", " ").split('\\')[-1]								# Get final file or folder from path
	error = False																	# Empty error variable, will be used to hold potential error return strings

	# Initialised variables
	unconfirmedYear, year = 0, 0

	try:
		unconfirmedYear = re.findall(r'\(\d{4}\)', filename)
		if unconfirmedYear[0] and len(unconfirmedYear) is 1:
			year = unconfirmedYear[0].replace(')',"").replace('(',"")					# If a year in brackets eg (2000) is found and only one found, chances are this is the year.
	except:
		if debug:
			print("-- Debug: Failed to match a year in standard brackets. Let's try again...")
		try:
			# Attempt a match with square brackets
			unconfirmedYear = re.findall(r'\[\d{4}\]', filename)
			if unconfirmedYear[0] and len(unconfirmedYear) is 1:
				year = unconfirmedYear[0].replace(']',"").replace('[',"")				# If a year in brackets eg (2000) is found and only one found, chances are this is the year.
		except:
			if debug:
				print("-- Debug: Failed to match a year in square brackets. Let's try again...")
			try:
				# Attempt to search for 4 digit number. Should avoid "1080p" and such because we're only searching " XXXX " with a space (dots were converted to spaces)
				unconfirmedYear = re.findall(r' \d{4} ', filename)
				if unconfirmedYear[0] and len(unconfirmedYear) is 1:
					year = unconfirmedYear[0].strip()									# Remove any unwanted whitespace
			except:
				if debug:
					print("-- Debug: Failed to match a 4 digit number in the string with whitespace or dots.")

	# Debug testing
	if debug:
		print("Path = "+path)
		print("'"+str(year)+"'")
		utilities.writeLine()

	currentYear = int(date.today().strftime("%Y"))										# Current year, used as a reference for how high a year should be (+3 years over just in case)
	if (year == 0):
		error = "Failed to find a suitable year match. This title should be confirmed by the user."
	else:
		error = "Detected year is not within expected year range of (1888-"+str(currentYear+3)+")"
	
	# Will return either a valid number or 0, indicating fail (and a error)
	return (year, error)
		

	
	
def getName(path, debug, year=None):

	try:
		title = stripBadCharacters(path).replace("."," ").replace(')',"").replace('(',"").replace(']','').replace('[','').split(year)[0].strip().split("\\")[-1]

		return title
	except:
		return False

def stripBadCharacters(x):
	# This function should be used to remove specific characters from an input and return it.
	
	return x