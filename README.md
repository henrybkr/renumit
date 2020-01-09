<p align="center"><img src="https://github.com/henrybkr/renumit/blob/master/data/logo_1.png" width="350"></p>

# 'Renumit'
> Deriving from the Romanian word name for 'renamed' but also 'renowned' or 'famous'. I can be considered something of a play on words. In the Romanian language 're' refers to 'again' whereas 'numit' refers to being 'named'.

## Important Notes
* This application is currently in development and not yet ready for use!
* Currently only supported on Windows - Testing on Windows 10

## About

This is another personal project this time making use of python to build a CLI based application for the sorting personal media. The job of this application is to take given file paths parameters and make assumptions in order to sort them in a desired way. The primary focus will firstly be the sorting movie files into a chosen directory.

This is a re-write of an existing functional, yet messy application. The idea is to make the existing app more modular and readable in order to improve chances of later extending it's functionality.

## Current Features
* Interaction with the [TMDb](https://www.themoviedb.org/) API
* Configurable user preferences
* Duplication helper utility
* Basic menu launched when not launched with parameters
* Run basic api call tests to confirm api is reachable

## Features in Progress
* Rename based on TMDB api call results
* Handle multiple file path inputs during the sorting process
* Functionality to review files based on their name and directory
* Functionality to review files based on their MediaInfo
* Debug option in the config file to confirm actions and output additional information to the user
* Produce a preview of renames before attempting to move anything

## Features to Implement
* Greater communication and involvement of the duplication utility script - currently operation mostly separately
* Produce a full list of required python libraries for this application
* History logs for each time the tool completes a rename with potential undo feature
* API interaction for TheTVDB and OMDb as alternatives to TMDb
* Offer configurable naming formats for the output filenames
* Capability of dealing with bonus "extra" content not typically found on a media database such as "behind the scenes"
* Remove unwanted keywords from files that are not directly renamed
* Configurable option to delete/recycle unwanted filetypes or specific filenames
* Configurable option to remove specific metadata from (for now just) MKV file formats such as track names
* Read and sort television series
* Capability of comparing potential user duplicates and automatically decide which one to keep.

## Technologies Utilised
* [Python 3.7.3](https://www.python.org/)
* [MediaInfo](https://mediaarea.net/)
* [tmdbsimple](https://github.com/celiao/tmdbsimple) via [TMDb](https://www.themoviedb.org/)
* [send2trash](https://github.com/hsoft/send2trash) - Cross-platform recycle/trash library
* [terminaltables](https://github.com/Robpol86/terminaltables) - Table drawing for console applications