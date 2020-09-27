<p align="center"><img src="data/logo_1.png" width="400"></p>

# 'Renumit' Changelog
> Overview of changes made to the app.

## 2020-09-27
* Minor update for bluray source detection.
* Minor text replacement string update.
* Update to preference configuration - Switched to JSON format with a nested format. Note - Empty config file output coming in next update for when not present. Example file provided though.
* Removed some redundant config settings.
* Added some future config settings references.
* Provided support for new JSON config format - Will likely be some bugs.

## 2020-05-25
* Now replaces 'bad' characters in titles with English versions. This should later be configurable.
* String detection on title for certain symbols such as colons that are refused by Windows. "Example: A documentary" becomes "Example - A documentary". Will later be configurable.
* String replacement support for time strings via regex eg "10:30" becomes "10-30" whilst still working as usual with above replacements.
* Additional check for 'WEB' source content included. Done as a final check because ' web ' can often be included in a movie title.
* Minor updates to movie edition detections.
* Fix for single file path input not being found as the 'main' movie file. 
* Remove unnecessary whitespace from output filenames.
* Bugfix for still using input year as output year. Now always using TMDB year and title rather than input.
* Feature to find best match without providing a year. Bases the final 'best decision' on any name/year collected from original file/folder. Requires more testing but appears to be working as intended.
* Confined the mediainfo text being searched for codec on mediainfoReview function (fixes issue where bad title returns incorrect codec).

## 2020-05-18
* Soundtrack sorting improvements, now sending to either 'Soundtracks' or 'Soundtracks/Example Folder' directories dependent on input path structure.
* Improved sorting of non-mkv files when told to do so in config. Note that filenames are not changed at all at this point. This also allows all filetypes, including likely unwanted filetypes.
* Dynamic output directory. The user can define either a constant output location (eg. 'sorted_location = "C:\example"') which potentially moves across drives or a relative location based on the input file (eg. sorted_location = "***\example").
* Bugfixes for preferences.config output and updated to latest required layout.
* Basic instructions & licence documentation for GitHub

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