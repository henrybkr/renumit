# -*- coding: utf-8 -*-

##########################################################################################################################
## This file contains functions that have the intention of modifying files.												##
##########################################################################################################################

# Required imports
import sys
from os.path import dirname, abspath
from os import system
from ..scripts import utilities
import subprocess
#from progress.bar import Bar

def updateTracks(filePath, config):
	response = [False, "Unknown Error with updateTracks function."]																																						# Default response, fails unless confirmed otherwise.
	propEditDir = dirname(dirname(dirname(abspath(__file__))))+"\\binaries\\mkvpropedit.exe"

	#utilities.printColor("orange", config, always=True)

	if utilities.checkExist(propEditDir):

		if config[0] and config[1]:
			subprocess.call([propEditDir, filePath, "--delete-attachment", "1", "--delete-attachment", "2", "--delete-attachment", "3", "--delete-attachment", "4", "-d", "title", "-t", "global:"],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
			response = [True, ""]
		elif config[0]:
			subprocess.call([propEditDir, filePath, "--delete-attachment", "1", "--delete-attachment", "2", "--delete-attachment", "3", "--delete-attachment", "4"],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
			response = [True, ""]
		elif config[1]:
			subprocess.call([propEditDir, filePath, "-d", "title", "-t", "global:"],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
			response = [True, ""]
		else:
			utilities.printColor("red", "-- Error: modifyFiles.updateTracks error!", always=True)
			response = [False, "Error launching correct subprocess command."]
		
	else:
		response = [False, "mkvpropedit.exe missing."]
	return response
	
