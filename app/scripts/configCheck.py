# -*- coding: utf-8 -*-

##########################################################################################################################
## A validator for config data received. Basically confirm the api keys work, output location exists					##
## 	and there are no invalid characters.																				##
##########################################################################################################################

# Required imports
import sys
sys.path.insert(1, r'\app\scripts')
sys.path.insert(1, r'\app\api')
import utilities, tmdbHelper # pylint: disable=import-error
import json

# Primary area for confirming api keys are valid
def apiKeyLocator(data):
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

	# TMDb
	if api == "tmdb":
		data = tmdbHelper.test(key)
		utilities.writeLine()
		
		# Now we have some data, check that it's useful and not an error message etc.
		if data:
			try:
				tmdb_title = data['results'][0]['title']
				if debug:
					print("TMDb title response: "+tmdb_title)
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
	
		#return testResult

	#result2 = tmdbHelper.search(key, "The Simpsons Movie", 2007)					# Request data from TMDb on given query.

	#print(result)
	
	
	
	
	# TMDb
	if api is "tmdb":

		
		return True
	# TheTVDB
	elif api is 2:
		print("Should work on TVDB mode here.")
		return True
	# OMDb
	elif api is 3:
		print("Should work on OMDB mode here.")
		return True
	else:
		print("-- Error: Problem selecting mode in apiKeyChecker")
		return False
	
