# -*- coding: utf-8 -*-

##########################################################################################################################
## ~ A supporting python script to check dropped folders (for now only folders) against other folders found in other    ##
##   locations - for example on another HDD. The aim is to only highlight potential dupes so the user can take action.  ##
## ~ Includes an 'empty folder' check feature with the option to delete them if requested.
##########################################################################################################################

import os
import sys
from os.path import join
from difflib import SequenceMatcher
import shutil																		

line = "--------------------------------------------------------------------------------"		# Random string to output a "line"
name_lists = []																					# Variable to retain multiple lists of "names"
total_dupes = 0																					# Variable to retain total number of dupes located.

#G:\#renumit
#H:\Movies TWO
#O:\Movies THREE

#E:\Renumit_sorted

## Note to self, for now, always put the first location as the one you want to move to a dupe folder.
locations_to_check = ['O:\Movies THREE', 'F:\Renumit_Sorted']

# Function to grab a list of all subfolder names of a given path and return it as an array/list.
def get_list(input_path, append=None):
	dirs = (os.listdir(input_path)) # current level

	if append:
		name_lists.append(dirs)
	else:
		return dirs


def confirm(message):												# User confirm with y or n characters. Returns true or false.
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

# Function to check for empty folders and delete them if requested.
def check_for_empty_subfolders():
	
	try:
		# Collect some input from the user.
		our_path = input("Please enter your exact path. Example: C:\Example\n")
		our_folders = get_list(our_path)
		empty_array = []
		
		# Loop through each folder and append to the empty list if an empty subfolder is located.
		for p in our_folders:
			dir = our_path+"\\"+p
			#print(dir)
			if not os.listdir(dir):
				empty_array.append(dir)
			
		# Only continue if the empty array is populated.
		if empty_array:
			# List all empty subfolders to the user.
			print("List of empty subfolders:\n"+line)
			for x in empty_array:
				print(x)
				
			# Ask if the user would like for the list of empty folders to be deleted or not.
			check = confirm("Would you like to delete the empty folders we find?")
			if check:
				for x in empty_array:
					os.rmdir(x)
				print(" -- Done!")
		else:
			print(line+"\nNo empty folders!\n"+line)
	except:
		print(line+"\nWhoops, we ran into an issue checking for empty subfolders :(\n"+line)

# Function to check dupes between multiple folders. Currently hardcoded to check specific folders.
def dupe_check():

	potential_move_queue = []										# Array to hold a list of locations of files the user might want to later delete

	try:
		if locations_to_check:
			print("\n")												# New like, improved formatting
			for x in locations_to_check:
				print("Making list of: '"+x+"'.")
				get_list(x,1) 										# Include an optional parametor used to append for the get_list function
			print("-- Done!\n")
		
		if name_lists:
			global total_dupes
			for x in name_lists[0]:
				for y in name_lists[1]:
					if x == y:
						total_dupes+=1
						location_1 = locations_to_check[0]+"\\"+x
						location_2 = locations_to_check[1]+"\\"+y
						
						potential_move_queue.append(location_1)	# append this location to array for potential later use.
			
			if potential_move_queue:
				## Print out the full list of all located duplicates to the user (and a total tally)
				print(line+"\nAll Located Duplicates:\n"+line)
				for y in potential_move_queue:
					print(y)
				print(line+"\nTotal: "+str(total_dupes)+"\n")
				
				# Now offer the user the chance to delete the list of dupes immediately.
				
				dupe_move_loc = locations_to_check[0].split("\\")[0]+"\\#dupes\\"	# Collect the root HDD in user (first location) + \#dupes to the string

				if confirm("Would you like to move these dupes to: '"+dupe_move_loc+"' ?"):
					print("Okay, let's move them...\n")
					
					
					
					for q in potential_move_queue:
						#print("moving --> "+potential_move_queue[q])
						shutil.move(q, dupe_move_loc)
					print("-- Done!")
				else:
					print("Okay, we won't delete anything!\n")
			else:
				print(line+"\nYay, no duplicates found!\n"+line+"\n")
			
		else:
			print(line+"\nWarning: Empty name_list array\n"+line)
		
	except:
		print(line+"\nWhoops, we ran into an issue with the dupe_check function :(\n"+line)
		raise



# ----------------------------------
# Main program functionality / menu |
# ----------------------------------
try:
	print(line)
	print("Welcome to the Renumit dupe utility.")
	print(line)
	
	
	app_running = True	
	# App is on a loop so when each function ends it returns the user to the menu
	while app_running:
		# User Menu, additional loop to gain valid input from the user and catch errors.
		user_choice = False
		while user_choice == False:
			
			print("User Menu:")
			print("0 - Exit application\n1 - Main dupe check functionality\n2 - Clear empty subfolders from a path\n")
			
			answer = input("Enter Mode: ")
			
			try:
				mode_select = int(answer)
				if mode_select == 0:
					user_choice = True
					app_running = False
					print("Exiting application!")
				elif mode_select == 1:
					print("Let's check out those pesky dupes...")
					user_choice = True
					dupe_check()
				elif mode_select == 2:
					print("Let's look for empty folders...")
					print(line)
					user_choice = True
					# Launch the function
					check_for_empty_subfolders()
					
				else:
					print("Invalid input. Try again!")
				
				
			except ValueError:
				print("Non-number input. Try again!")

	print("Bye!")
	os.system("pause")

except Exception as e:
	# Print error info
	print("\n"+line+"\nError: ")
	print(str(e))															# Print exception
	
	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]						# Unpack system error info into variable
	print("Filename: "+fname+", Line Error: "+str(exc_tb.tb_lineno))		# Print error filename and line
	print(line+"\n")
	
	os.system("pause")
	raise