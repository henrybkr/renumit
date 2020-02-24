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
sys.path.insert(1, r'\app\sorting')
import utilities, mediaInfoReview # pylint: disable=import-error
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

def reviewPath(inputPath):

	path = (inputPath.split("\\")[-2])+"\\"+((inputPath.split("\\"))[-1])				# Note, this might pose issues later. It finds the parent directory and the main movie file (+ extension) used for reference
	altPath = path.replace(".", " ")

	# First attempt to collect info with the original path
	edition = getEdition(path)
	source = getSource(path)
	mediaInfoData = mediaInfoReview.basicInfo(inputPath)
	##print(mediaInfoData)
	

	# If any failed returns, attempt with the alt paths (periods replaced with spaces)
	if not edition:
		edition = getEdition(altPath)
	if not source:
		source = getSource(altPath)
	

	return {'edition': edition, 'source': source}

# Function to collect edition information from a provided path if available
def getEdition(path):
	ref = path.lower().replace("-"," ")
	edition = ""

	if (" criterion " in ref):
		edition = "Criterion"
	elif (" extended " in ref):
		edition = "Extended"
	elif (" rm4k " in ref) or ("4k remastered" in ref) or ("4k remaster" in ref) or (") rm (" in ref):
		edition = "Remastered"
	elif (" unrated " in ref):
		edition = "Unrated"
	elif (") dc " in ref) or (" dc (" in ref) or ("directors cut" in ref) or ("director's cut" in ref):
		edition = "Directors Cut"
	elif ("anniversary edition" in ref) or (" anniv" in ref) or (" anniversary" in ref):
		# anniversary edition. Collect XXth value
		try:
			num = re.findall(r" \d\dth ",ref)
			edition = str(num[0])[1:-1]+" Anniversary Edition"
		except:
			edition = "Anniversary Edition"
	elif (") se " in ref):
		edition = "Special Edition"
	elif (") ce " in ref):
		edition = "Collectors Edition"
	elif (" imax " in ref):
		edition = "IMAX"
	elif (" open matte " in ref):
		edition = "Open Matte"
	elif (") diamond (" in ref):
		edition = "Diamond Edition"
	elif (" final cut " in ref):
		edition = "Final Cut"
	
	return edition

# Function to collect source information from a provided path if available
def getSource(path):

	source = ""

	ref = path.lower().replace("."," ")		# Lowercase for easier querying
	
	if ("bluray" in ref) or ("bdrip" in ref) or ("blu ray" in ref) or (" bd " in ref) or ("blu-ray" in ref):
		source = "Blu-Ray"
	if ("hddvd" in ref) or ("hd-dvd" in ref):
		source = "HDDVD"
	elif ("dvd" in ref) or ("dvdrip" in ref) or ("dvd-rip" in ref):
		source = "DVD"
	elif ("web-dl" in ref) or ("web dl" in ref) or ("web x265" in ref) or ("web x264" in ref) or ("webrip" in ref) or ("web-rip" in ref) or ("web h.264" in ref) or ("web h.265" in ref):
		source = "WEB"
	else:
		return source
	
