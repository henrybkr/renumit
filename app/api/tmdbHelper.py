# -*- coding: utf-8 -*-

##########################################################################################################################
## Functionality used through the application to interact with The Movie Database (TMDb) API.							##
##########################################################################################################################

import tmdbsimple as tmdb

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
		print("blah")
		raise