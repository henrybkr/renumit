# -*- coding: utf-8 -*-

##########################################################################################################################
## Functionality used through the application to interact with The Movie Database (TMDb) API.							##
##########################################################################################################################

import tmdbsimple as tmdb
import os
import copy
from ..scripts import utilities
from difflib import SequenceMatcher

def test(key):
	tmdb.API_KEY = key																							# Set the api key to be used by tvdbsimple
	search = tmdb.Search()

	try:		
		response = search.movie(query="The Matrix",year=1999,include_adult=True)
		return response
	except:
		raise

def search(key, title, year=None):
	tmdb.API_KEY = key																							# Set the api key to be used by tvdbsimple
	search = tmdb.Search()
	
	try:
		# In the event a year isn't present in the title, allow for searching by title only.
		if year:
			response = search.movie(query=title,year=year,include_adult=True)
		else:
			response = search.movie(query=title,include_adult=True)
		
		return response
	except:
		print("-- Woah, TMDB search error!")
		raise


def compareTMDBNameYear(response, localNameYear, configJSON):

	myDebug = False

	#response = search(key, title, year)
	#utilities.printColor("yellow", response, always=True)
	#print(response[0])

	if int(response['total_results']) == 0:
		utilities.printColor("red", "Warning, no TMDB results for this title: "+localNameYear, always=True)
		return False
	else:
		bestResult = getLikelyMovieResult(response, localNameYear, configJSON)				# Run functionality to check between local file name and multiple TMDB results
		if bestResult:
			matchRate = max([bestResult[3], bestResult[4]])										# Collect the higher match ratio from the returned result.
			
			if matchRate == 1:
				if myDebug:
					utilities.printColor("green", "Perfect match found: "+str(bestResult[2]), always=True)
			elif matchRate >= configJSON['matchRate']:
				if myDebug:
					utilities.printColor("green", "Good match found: "+str(bestResult[2]), always=True)
			else:
				utilities.printColor("red", "The match: '"+str(bestResult[2])+"' --> '"+str(bestResult[0])+"' doesn't meet required ratio of: "+str(configJSON['matchRate']), always=True)
				return False

			# Assuming we have some data, return the final (standard) title and year
			title = bestResult[5][0]
			year = bestResult[5][1]

			return { 'title': title, 'year': year }
		else:
			utilities.printColor("red", "-- Warning: No TMDB search results.", always=True)
			return False
	

	



# Function to return the most likely result from the search data.
def getLikelyMovieResult(search_data, localNameYear, configJSON):

	myDebug = False
	compareList = []		# Default empty. Will hold compare data
	bestResultData = []		# Default empty. Will hold a result and the compare ratio.

	for s in search_data['results']:
		searchTitle = 				s['title']
		searchYear = 				str(s['release_date'].split("-")[0])
		searchNameYear = 			searchTitle+" ("+searchYear+")"				# Produces a name and year from the search data. Format = Name (XXXX)
		searchNameYear_altTitle = 	s['original_title']+" ("+searchYear+")"		# Same as above but with alternative original title.
		
		tvmb_match_ratio = SequenceMatcher(None, localNameYear.lower(), searchNameYear.lower()).ratio()
		tvmb_match_ratio_alt = SequenceMatcher(None, localNameYear.lower(), searchNameYear_altTitle.lower()).ratio()

		# Check for perfect match on standard title or 'original' title
		
		# This might need improving to check if there is more than one "perfect" match
		"""
		if tvmb_match_ratio == 1:
			return s
		elif tvmb_match_ratio_alt == 1:
			return s			
		"""
		compareList.append([searchNameYear, searchNameYear_altTitle, localNameYear, tvmb_match_ratio, tvmb_match_ratio_alt, [searchTitle, searchYear]])
	
	tableData = copy.deepcopy(compareList)																														# Make a copy of the list whilst removing any reference to original one (modifying it below)
	
	for row in tableData:
		del row[5]																																				# Remove this data from list, don't need to display it to the user.

	tableData.insert(0,["TMDB Title", "TMDB Alt Title", "Local Title", "Title Compare Rate", "Original Title Compare Rate"])									# Insert an extra row for table headings
	if myDebug:
		utilities.makeTable('Debug for Comparison Results', tableData)																								# Debug output

	# Assuming we haven't found a 'perfect' match at this point, loop through results to find the best option.
	# Return the highest scoring result.

	topResult = None
	for result in compareList:
		if topResult == None:
			topResult = result																# Sets the first result as the one to beat
		else:
			largestRatio = max([topResult[3], topResult[4]])								# Get the highest ratio of standard and original titles
			if result[3] > largestRatio or result[4] > largestRatio:						# Determine if this result is rated better than the current best
				topResult = result
	return topResult