# -*- coding: utf-8 -*-

##########################################################################################################################
## A validator for config data received. Basically confirm the api keys work, output location exists					##
## 	and there are no invalid characters.																				##
##########################################################################################################################

# Required imports
import sys
#sys.path.insert(1, r'\app\scripts')
#sys.path.insert(1, r'\app\api')

from . import utilities
from ..api import tmdbHelper

#import utilities, tmdbHelper # pylint: disable=import-error
import json

# Primary area for confirming api keys are valid
def apiKeyAvailable(data):
	# Loop through the received api json data to check existence of api keys
	
	# Basic check to confirm all api keys are present before moving on.

	numApis = len(data)	# Total number of api keys
	apiTally = 0
	for p in data:
		if p["key"]:
			apiTally+=1																				# Increment tally
	if not apiTally:
		return(0, "-- Error: No API keys found. Please enter one in the config file to continue!")	# no API keys available
	elif numApis-apiTally==1:
		return(1, "-- Warning: Missing "+str(numApis-apiTally)+" API key.")							# 1 API key missing
	elif numApis-apiTally>=2:
		return(1, "-- Warning: Missing "+str(numApis-apiTally)+" API keys.")						# 2 or more
	else:
		return (2, "-- Info: All API keys located.")												# All API keys located.

# Functionality used for testing that api's are operational with a specified search. Offers debug mode to output the received string to the user if desired.
def apiTest(api, key, debug=None):
	#result = None																					# Initialised as empty. Will fail if not changed.
	
	try:
		# TMDb
		if api is "tmdb":
			data = tmdbHelper.test(key)
			print(utilities.line+"\n")																									# Extra new line for improved presentation.
			
			# Now we have some data, check that it's useful and not an error message etc.
			if data:
				try:
					tmdbTitle = data['results'][0]['title']
					
					if tmdbTitle == "The Matrix":
						utilities.printColor('green', "-- Info: Good response from TMDb.", debugMode=debug)
						return True																											# Provide confirmation working as expected
					else:
						if debug:
							print("-- Debug Warning: Api response not as expected. Response: "+tmdbTitle+" (Expected 'The Matrix')")		# Debug warning
						else:
							print("-- Error: TMDB API response received but is not as expected. Consider confirming via debug mode.")		# Standard user warning
						
				except:
					if debug:
						print("-- Debug: Data from TMDb was returned, but no title was located. Response from TMDb:")
						utilities.writeLine()
						print(data)
						utilities.writeLine()
					return False
			else:
				if debug:
					print("-- Debug: TMDb test returned no data.")
				return False
		
		elif api is "tvdb":
			utilities.printColor('yellow', "-- Warning: TVDB check not yet functional.", debugMode=debug)
			return False
		# OMDb
		elif api is "omdb":
			utilities.printColor('yellow', "-- Warning: OMDb check not yet functional.", debugMode=debug)
			return False
		else:
			utilities.printColor('red', "-- Error: Problem selecting mode in apiKeyChecker.", always=True)
			return False
	except:
		utilities.printColor('red', "-- Error: Error with api apiTest.", always=True)
