<p align="center"><img src="https://github.com/henrybkr/renumit/blob/master/data/logo_1.png" width="350"></p>

# 'Renumit Changelog'
> Overview of changes made to the app.

## 2020-04-13
* At this point, it's fairly usable for movies, although you should check renames before confirming. Must currently enable the debug flag in the config file.
* Folder clean-up: Will now detect and delete any empty directories after a rename.
* Improvements when dealing with both a file input (example 'file.mkv') and folder paths.
* Switched to more standard approach with how modules/classes are imported arround the application.
* Fix not picking up 'WEB' as a source type.
* Presentation improvements and minor fixes for the rename preview. Displays a clearer view of all 'extra' files for a movie.
* Visual loading bars for filename reviews and the actual rename processes.
* Ability to skip or delete empty 'main' movie files (0 bytes) or directories without a 'main' movie file in debug mode. -- Note that this currently skips directory with only a 'extras' directory, etc.
* New logo for GitHub page & added ascii art on menu load. Other minor changes to intro presentation.
* Start of changelog updates.