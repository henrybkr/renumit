<p align="center"><img src="data/logo_1.png" width="400"></p>

# 'Renumit' Changelog
> Overview of changes made to the app.

## 2020-05-10
* Now in a usable state again, bug fix for multiple results in TMDB search being found.
* Now compares all TMDB results received and looks for most appropriate in search results to use for rename title and year.
* Added support for sorting into a soundtrack directory (mp3, wav, flac & m4a)
* Pulled back on assumption we want to delete non-video files immediately. Replaced with highlighting non-video files in rename preview debug table with red arrow. Note, not currently moving non-video files.

## 2020-05-07
* Bug fix for detection of non-video files in the 'main directory' area.
* Start of TMDB feature integration to check for correct titles and years. Currently only works when there is one search result.

## 2020-04-25
* Further Plex support for extra folders, sending certain detected filenames to folders such as 'Trailers' and 'Deleted Scenes'. 
* Display a few user preferences before confirming renaming when in debug mode.
* Change to config handling for determining whether to remove mkv covers. Can now enter 'false' for no action, 'true' for apply to all files, or 'true extras' for applying to only extra files.
* Now displays moving errors in a table, displaying the exact error that caused the failure. Only displays when issues are present.
* New config feature to remove video MKV titles, same options as dealing with covers (false, true, true extras).
* Config features for title and cover are now put to use. During the actual moving process mkvpropedit is used to modify the file if the user has configured it to do so.
* Bugfix for non-mkv files breaking the renaming process.
* Solved issue where provided paths only include unaccepted files paths which broke the renaming process.

## 2020-04-13
* At this point, it's in a fairly usable beta state for movies. You should check any renames before confirming. Must currently be ran using debug mode. Enable the debug flag via the config file.
* Folder clean-up: Will now detect and delete any empty directories after a rename.
* Improvements when dealing with both a file input (example 'file.mkv') and folder paths.
* Switched to more standard approach with how modules/classes are imported around the application.
* Fix not picking up 'WEB' as a source type.
* Presentation improvements and minor fixes for the rename preview. Displays a clearer view of all 'extra' files for a movie.
* Visual loading bars for filename reviews and the actual rename processes.
* Ability to skip or delete empty 'main' movie files (0 bytes) or directories without a 'main' movie file in debug mode. -- Note that this currently skips directory with only a 'extras' directory, etc.
* New logo for GitHub page & added ascii art on menu load. Other minor changes to intro presentation.
* Start of changelog updates.