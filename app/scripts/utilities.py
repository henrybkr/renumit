# -*- coding: utf-8 -*-

##########################################################################################################################
## Utility script that contains a handful of functions used throughout the application.									##
##########################################################################################################################

import os
from terminaltables import AsciiTable
from send2trash import send2trash
from os.path import join
import time
from pathlib import Path

line = "--------------------------------------------------------------------------------------------------"
clear_win = lambda: os.system('cls')											# Empty (windows) cmd window

# Function to output an introduction to the tool.
def intro(path):

	menu_file = path+r"\\data\\menu_ascii.txt"																			# Expected relative path to the renumit config file.

	with open(menu_file) as f: # The with keyword automatically closes the file when you are done
		printColor("yellow", "\n ~~ Presenting ~~ ", always=True)
		printColor("orange", f.read(), always=True)

	printColor("yellow", "\n"+line+"\n                              -- A media renaming script by hbkr --                               \n"+line+"\n", always=True)			# Output introduction to user.

# Returns the list of filepaths provided if any.
def getValidPaths(debugMode, filePaths=None):
	print("")																																# New line for presentation purposes
	writeLine()
	validPaths = []
	hasInvalidPaths = False

	# Check if the user has provided filepaths to the application.
	if filePaths:
		for path in filePaths:

			if checkExist(path):
				if (getDirFileSize(path) == 0):
					hasInvalidPaths = True
					printColor("yellow", "-- Warning: The following path is empty or has only empty files:", debugMode=debugMode)
					printColor("standard", '-→ '+path, debugMode=debugMode)
					if (confirm("Do you wish to delete this folder now?")):
						deleteEmptyDirs(path)
					else:
						printColor("standard", "-- Info: Okay, skipped this one!", debugMode=debugMode)
				else:
					validPaths.append(path)																									# This path has something inside that the application can analyse, so it's a valid path, append it to the array.
			else:
				hasInvalidPaths = True
				printColor("yellow", "-- Warning: The following path doesn't exist:", debugMode=debugMode)
				printColor("standard", '-→ '+path, debugMode=debugMode)
		
		if hasInvalidPaths:
			writeLine()
		return validPaths																													# Once the for loop has finished, returned the list of 'valid' paths.

	else:
		return False

# The menu itself, displaying information to the user.		
def menu():
	user_choice = False
	
	# Begin menu loop.
	while user_choice == False:
		# Provide a menu with a range of options.
		print("\nMain Menu: What would you like to do?\n")
		print("0 - Exit")
		print("1 - Check Renumit can communicate with an API")
		print("2 - Dupe Check functionality (unavailable)")
		print("3 - Update your configuration file (unavailable)")
		print("4 - Sample mode - See how a rename would look (unavailable)")
		
		answer = input("\nPlease enter the number of your choice: ")
		try:
			menuChoice = int(answer)																					# Make sure answer is a valid integer. Exception occurs if not.
			
			# Deal with user's menu choice
			if menuChoice == 0:
				# Exit application
				user_choice = True																						# Confirm user has made a choice allowing exit of menu.
				return [0,0]																							# Should be interpretted as [menu loop can end, option was exit]
			elif menuChoice == 1:
				# Check Renumit can communicate with an API 
				user_choice = True																						# Confirm user has made a choice allowing exit of menu.
				return [1,1]																							# Should be interpretted as [menu loop can continue, option was api check]
			else:
				print("Invalid input. Try again!")
		except ValueError:
			print("Non-number input. Try again!")
		except:
			print("Hmm, invalid input on the menu or something.")

# Continues to display the menu till the application is told to exit.
def beginMenu():
	# Make sure the menu is consistently displayed until a exit command is given.
	
	appContinue = True
	while appContinue == True:
		menuResult = menu()																								# Present menu to user
		if menuResult[0] == 0:
			appContinue = False																							# If the result is 0, end the while loop, ending the application.
		else:
			print("\nMenu option was successfully chosen. However, functionality not currently there.")					# Here we should launch the additional options in the menu. Might want to launch them from the menu utility itself, idk.


# Function to write a single line to the cli
def writeLine():
	print(line)

# Function to confirm that a given path exists or not.
def checkExist(path):
	if os.path.exists(path):
		return True
	else:
		return False
		
# Function to gain user confirmation with y or n characters. Returns true or false. Optional message input parameter.
def confirm(message):
	while True:
		if message:
			answer =  input("\n"+message+" (Y/N): ").lower()
		else:
			answer =  input("Confirm (Y/N): ").lower()

		if answer == "y":
			return True
		elif answer == "n":
			return False
		else:
			print("Invalid input. Try again!")

# Function to read all paths from a set of given lists if they exist.
def pathValidityDebug(validPaths, invalidPaths):
	if validPaths:
		print("\nDebug -- Valid Paths:\n"+line)
		for filePath in validPaths:
			print(filePath)	
	if invalidPaths:
		print("\nInvalid Paths:\n"+line)
		for filePath in invalidPaths:
			print(filePath)

	# Since this is a debug mode option, the list is displayed but time is given to review it before moving to the next step
	print("\nReady to continue?\n")
	os.system("pause")

def reportErrors(filePaths, invalidPaths, sortingErrors):
	# Report errors from the related error arrays if errors exist.

	if invalidPaths or sortingErrors:																					# Only continue if any errors actually exist.
		print("\nWhoops, looks like we've got some errors...\n")														# Generic user feedback
		invalidTableData, renameErrorTableData = [], []																	# Table data lists
		# invalidPaths first
		for i in invalidPaths:
			invalidTableData.append([i,"Path invalid"])																	# Includes a generic invalid path message. Might need revisiting later if multiple invalid filepath possibilities (read errors, etc)
		# Now for rename errors
		for r in sortingErrors:
			renameErrorTableData.append([r['path'], r['error']])														# Include both the path and the error
		# Now let's look at displaying the error results to the user
		if invalidPaths:
			print(AsciiTable(invalidTableData, "Invalid Paths").table)													# Print the table of errors
		if sortingErrors:
			print(AsciiTable(renameErrorTableData, "Sorting Errors").table)												# Print the table of errors


def renameTable(renameArray, debugMode):
	if debugMode:

		if len(renameArray) > 0:

			tableData = [(getColor("orange","Original Path"), getColor("orange","New Path"))]

			for x in renameArray:
				if x[2]:
					if not "mkv" in x[0] and not "mp4" in x[0]:																			# Included check for acceptable file formats. Indicate that action can be taken for this file
						y = getColor("red","―→ ")+x[0]																			# Produce a little bump, highlighting it's a "main" file
						z = getColor("red","―→ ")+x[1]																			# Produce a little bump, highlighting it's a "main" file
					else:
						y = getColor("orange","―→ ")+x[0]																		# Produce a little bump, highlighting it's a "main" file
						z = getColor("orange","―→ ")+x[1]																		# Produce a little bump, highlighting it's a "main" file
					tableData.append((y, z))
				else:
					if not "mkv" in x[0] and not "mp4" in x[0]:																			# Included check for acceptable file formats. Indicate that action can be taken for this file
						y = getColor("orange","|")+getColor("red", "――→ ")+x[0]																		# Similar to above, indicate it's a extra with a larger arrow.
						z = getColor("orange","|")+getColor("red", "――→ ")+x[1]																		
					else:
						y = getColor("orange","|――→ ")+x[0]																		# Similar to above, indicate it's a extra with a larger arrow.
						z = getColor("orange","|――→ ")+x[1]																		
					tableData.append((y, z))

			if tableData:
				print("\n" + AsciiTable(tableData, "Rename Preview (Debug enabled)").table)
			else:
				printColor("yellow", "Warning -- Looks like we have no rename data to display.")
			return True

		else:
			return False


# Output the full list of confirmed names/years in table format
def nameYearTable(array):
	try:
		if array[0]:
			tableData = []
			for y in array:
				tableData.append([y['title'], y['year']])
			
			temp = tableData
			temp.insert(0,[getColor('orange','Title'),getColor('orange','Year')])
			print("\n"+AsciiTable(temp, "Movie Names/Years").table+"\n")												# Print the table
	except:
		print("Warning -- Error with nameYearTable function.")


def deleteOrIgnore(config, debug, x):

	debug = False

	conf = config['nonVideoFiles'].lower()

	if debug:
		print(("Debug -- deleteOrIgnore decision for file: '"+x+"' --> ")+(getColor("yellow", conf)))

	if conf == "delete":
		print("--> Run code to delete -->" + "'" + x + "'")
	elif conf == "recycle":
		send2trash(x.replace('\\\\','\\'))                                                      					# Recycle functionality
		if checkExist(x):
			if(debug):
				printColor("yellow", "Recycled the file: '"+x+"'.", debug)
			return { 'issue': True, 'message': "Warning -- Attempted to recycle '"+x+"' but it still exists.", 'shouldRename': False }
	else:
		if debug:
			print("--> User config says we don't need to delete --> " + "'" + x + "'")
		return { 'issue': False, 'shouldRename': True }

	

def addSpaces(inputString, spaceChar):
	if str(inputString) != "":
		return str(inputString)+spaceChar
	else:
		return ""

def printColor(color, string, *args, **kwargs):																			# Function to output string as a colour
	always = kwargs.get('always', False)
	debugMode = kwargs.get('debugMode', False)
	if (always is True) or (debugMode is True):
		my_color = ""
		if color is "green":
			my_color = "\033[1;32;40m"
		elif color is "red":
			my_color = "\033[1;31;40m"
		elif color is "yellow":
			my_color = "\033[1;33;40m"
		elif color is "cyan":
			my_color = "\033[1;36;40m"
		elif color is "purple":
			my_color = "\033[1;35;40m"
		elif color is "orange":
			my_color = "\033[38;5;214m"
			
		if my_color != "":
			print(my_color+str(string)+"\033[0m")
		else:
			print(str(string))

def getColor(color, string):
	my_color = ""
	if color is "green":
		my_color = "\033[1;32;40m"
	elif color is "red":
		my_color = "\033[1;31;40m"
	elif color is "yellow":
		my_color = "\033[1;33;40m"
	elif color is "cyan":
		my_color = "\033[1;36;40m"
	elif color is "purple":
		my_color = "\033[1;35;40m"
	elif color is "orange":
		my_color = "\033[38;5;214m"
		
	if my_color != "":
		return(my_color+string+"\033[0m")

def recycleFolder(inputPath):
	try:
		#print("Nothing here! Can be deleted!")                                                     # Confirmed no remaining files or subfolders. Delete.
		send2trash(inputPath.replace('\\\\','\\'))                                                      # Recycle functionality
		if os.path.exists(inputPath):
			print("Failed to delete.")
			return False                                                                       # Add the issue to the cleanup error array
		else:
			return True
	except PermissionError:
		print("Error_501: Don't have permission to recycle folder!")
		return False
##########

def deleteEmptyDirs(inputDir):												# Function used to clear up empty folders (usually after they have been moved)
	my_filepath = inputDir
		
	if os.path.exists(my_filepath):
		for root, dirs, files in os.walk(my_filepath,topdown=False):
			for name in dirs:
				fileName = join(root,name)

				# _ is a dummy variable, but normally it would be the directory path for os.walk
				for _, dirnames, files in os.walk(fileName):
					#print("dir length = ", dirpath,len(dirnames))
					if files:
						#print("File exists here, can't delete yet.")                                               # When a file still remains, break
						##c.append([fileName]) 
						break
					elif len(dirnames) != 0:
						#print("Directory exists here with subfolder/file inside, can't delete yet.")               # When a subfolder still remains, break
						##c.append([fileName])
						break
					else:
						try:
							#print("Nothing here! Can be deleted!")                                                     # Confirmed no remaining files or subfolders. Delete.
							send2trash(fileName.replace('\\\\','\\'))                                                      # Recycle functionality
							if os.path.exists(fileName):
								print("Failed to delete.")
								##c.append([fileName])                                                                       # Add the issue to the cleanup error array
						except PermissionError:
							#printColor("red", "Error_501: Don't have permission to recycle folder!", debugMode=True)
							##c.append([fileName])
							pass
						#else:                       
							#print("RECYCLED!")	

		# Now check if the root folder can be deleted
		if os.path.exists(my_filepath):
			# _ is a dummy variable, but normally it would be the directory path for os.walk
			for _, dirnames, files in os.walk(my_filepath):
				if files:
					break
				elif len(dirnames) != 0:
					break
				else:
					try:
						#print("Nothing here! Can be deleted!")
						send2trash(my_filepath.replace('\\\\','\\'))													# Recycle functionality
					except PermissionError:
						##if debug:
						printColor("red", "Error_502: Don't have permission to recycle folder!", debugMode=True)
						##c.append([my_filepath])
	else:
		if not (".mkv" in my_filepath or ".mp4" in my_filepath):
			printColor("yellow", "-- Warning: Fail to delete empty directory. Likely already deleted! (error 20)", debugMode=True)

# Collect the size (in bytes) of a given path directory.
def getDirFileSize(path):
	# For file input
	if os.path.isfile(path):
		return os.path.getsize(path)
	# For directory input
	elif os.path.isdir(path):
		return sum(f.stat().st_size for f in Path(path).glob('**/*') if f.is_file())
	# Error handling
	else:
		# Error handling
		printColor("red", "-- Error: Can't determine if this is a file or folder to run validity checks (getDirFileSize).", debugMode=True)
		return 0

def configTable(configData):
	if configData:
		tableData = []
		tableData.append([getColor("orange", "Your Sorting/File Modification Preferences"), getColor("orange", "Value")])
		tableData.append([getColor("orange", "→")+" Remove covers from MKV's?", mainExtrasStringSwitch(configData['removeCovers'])])
		
		tableData.append([getColor("orange", "→")+" Remove video titles from MKV's?", mainExtrasStringSwitch(configData['removeMKVTitle'])])
		tableData.append([getColor("orange", "→")+" Keep non-MKV Files?", configData['keepNonMkv']])
		tableData.append([getColor("orange", "→")+" What to do with non-video files?", configData['nonVideoFiles']])

		print("\n"+AsciiTable(tableData).table)													# Print the table of errors
	else:
		printColor("red", "-- Error: Missing configData for configTable feature.", always=True)

# Basic 'switch' implementation for outputting a string based on input string number input. Used a few times.
def mainExtrasStringSwitch(stringValue):
	#print(stringValue)
	num = int(stringValue)								# Convert the string number value to an integer.
	switcher = {
		0: "False / No Action",
		1: "Apply to all files",
		2: "Apply to extras only",
	}
	return switcher.get(num, "Invalid month")

def failedMoveTable(issueArray):

	failTable = []

	failTable.append([getColor('orange', 'Original Filename'), getColor('orange', 'Expected New Filename'), getColor('orange', 'Error')])
	for issue in issueArray:
		failTable.append([issue[0][0], issue[0][1], issue[1]])

	print("\n"+AsciiTable(failTable, getColor("red", "Moving Errors")).table)


def makeTable(title, data):
	print("\n"+AsciiTable(data, getColor("red", title)).table)

# Function to produce a relative output directory based on config file.
def getRelativeOutputPath(path, sortedDirString):
	drive = os.path.splitdrive(path)
	outputPath = sortedDirString.replace("***", drive[0]+"")

	# Double check we don't have extra backslashes for our new directory.
	if "\\\\" in outputPath:
		outputPath = outputPath.replace("\\\\", "\\")

	return outputPath

# Function to make a directory without any user input.
def forceMakeDir(path):
	if not checkExist(path):
		os.makedirs(path, mode=0o777, exist_ok=False)										# Create content directory

		if checkExist(path):
			return True
		else:
			return False
