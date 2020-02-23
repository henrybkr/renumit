# -*- coding: utf-8 -*-

##########################################################################################################################
## Utility script that contains a handful of functions used throughout the application.									##
##########################################################################################################################

import os
from terminaltables import AsciiTable

line = "--------------------------------------------------------------------------------"
clear_win = lambda: os.system('cls')											# Empty (windows) cmd window


# Function to output an optional introduction to the tool. Returns the list of filepaths provided if any.
def intro(filePaths=None):
	print(line+"\n-- Welcome to Renumit, a tool used for renaming media files --------------------\n"+line+"\n")			# Output introduction to user.
	
	# Check if the user has provided filepaths to the application.
	if filePaths:
		return filePaths																									# Return the list of filepaths
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
		menuResult = menu()				# Present menu to user
		if menuResult[0] == 0:
			appContinue = False			# If the result is 0, end the while loop, ending the application.
		else:
			# Here we should launch the additional options in the menu. Might want to launch them from the menu utility itself, idk.
			print("\nMenu option was successfully chosen. However, functionality not currently there.")		


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

	if invalidPaths or sortingErrors:											# Only continue if any errors actually exist.
		print("\nWhoops, looks like we've got some errors...\n")				# Generic user feedback
		invalidTableData, renameErrorTableData = [], []							# Table data lists
		# invalidPaths first
		for i in invalidPaths:
			invalidTableData.append([i,"Path invalid"])							# Includes a generic invalid path message. Might need revisiting later if multiple invalid filepath possibilities (read errors, etc)
		# Now for rename errors
		for r in sortingErrors:
			renameErrorTableData.append([r['path'], r['error']])				# Include both the path and the error
		# Now let's look at displaying the error results to the user
		if invalidPaths:
			print(AsciiTable(invalidTableData, "Invalid Paths").table)			# Print the table of errors
		if sortingErrors:
			print(AsciiTable(renameErrorTableData, "Sorting Errors").table)		# Print the table of errors

# Output the full list of confirmed names/years in table format
def nameYearTable(array):
	try:
		if array[0]:
			tableData = []
			for y in array:
				tableData.append([y['title'], y['year']])
			
			temp = tableData
			temp.insert(0,['\nTitle\n','\nYear\n'])
			print("\n"+AsciiTable(temp, "Confirmed Renames").table+"\n")		# Print the table
	except:
		print("Warning -- Error with nameYearTable function.")


def deleteOrIgnore(config, debug, x):
	if config['deleteNonVideos']:
		print("--> Run code to delete -->" + "'" + x + "'")
	else:
		print("--> User config says we don't need to delete --> " + "'" + x + "'")