<p align="center"><img src="data/logo_1.png" width="400"></p>

# 'Renumit'
> Deriving from the Romanian word for renamed, renowned or famous. In the Romanian language 're' refers to 'again' whereas 'numit' refers to being 'named'.

## Important Notes
* This application is currently in development but ready for testing using the debug flag in the .config file.
* Currently only supported on Windows - Tested via Windows 10.

## About
A personal project making use of python to build a CLI based application for the sorting personal media into desired naming schemes and folder structures. The job of this application is to take given file paths parameters, read from user preferences and make assumptions in order to sort them as instructed. The primary focus will firstly be the sorting movie files into a chosen directory but may later look into other areas such as TV and Anime content.

This is a re-write of an existing functional, yet messy application. The idea is to make the existing app more modular and readable in order to improve chances of later extending it's functionality.

## Usage
> renumit.py "path/to/your/media_folder"
> renumit.py "path/to/your/video.mkv"

## Current Features
* Interaction with the [TMDb](https://www.themoviedb.org/) API
* Produce new file structures for both a main movie file and any corresponding extras
* Move existing files/folder structures to the new preferred structure
* Configurable user preferences
* Able to accept either direct file path or directories as an input
* Duplication helper utility (Will be utilised properly soon)
* Configurable decisions to delete, recycle or skip over non-video files
* Basic menu launched when launched without parameters
* Run basic api call tests to confirm api is reachable
* Collect and make use of data found via original filename and video container MediaInfo
* Opportunity for a debug preview of renames before attempting to move anything and display some additional process information
* Cleans up after itself after renaming

## Changelog
<a href="changelog.md">Click here for changelog</a>

## Features in Progress
* Debug option in the config file to confirm actions and output additional information to the user
* Offer configurable naming formats for the output filenames
* Remove unwanted keywords from files that are not directly renamed
* Configurable option to delete/recycle unwanted filetypes or specific filenames
* Folder clean up functionality for after the sorting process 

## Features to Implement
* Greater communication and involvement of the duplication utility script - currently operating mostly separately
* Produce a full list of required python libraries for this application
* History logs for each time the tool completes a rename with potential undo feature
* API interaction for TheTVDB and OMDb as alternatives to TMDb
* Configurable option to remove specific metadata from (for now just) MKV file formats such as track names
* Read and sort television series
* Capability of comparing potential user duplicates and automatically decide which one to keep

## Technologies Utilised
* [Python 3.7.3](https://www.python.org/)
* [MediaInfo](https://mediaarea.net/)
* [MKVToolNix (mkvpropedit)](https://github.com/nmaier/mkvtoolnix)
* [tmdbsimple](https://github.com/celiao/tmdbsimple) via [TMDb](https://www.themoviedb.org/)
* [send2trash](https://github.com/hsoft/send2trash) - Cross-platform recycle/trash library
* [terminaltables](https://github.com/Robpol86/terminaltables) - Table drawing for console applications
* [progress](https://github.com/verigak/progress) - Easy progress reporting for Python

## Future Stuff
* Currently considering a C# implementation with a dedicated GUI for Windows OS'