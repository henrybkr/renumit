<p align="center"><img src="data/logo_1.png" width="400"></p>

# Documentation / Instructions

## General Usage
> renumit.py "path/to/your/media_folder"
> renumit.py "path/to/your/video.mkv"
> renumit.py          (Presented with a short menu when launching without any parameters)

## Configuration File

Edit the following .config file in your preferred text editor.
> Renumit/data/preferences.config

Note, if you don't see this file, launch the application once.

## Configuration Options

> Note, don't modify the structure or placement of anything in this file otherwise it will break the application. Only modify the values. Simply delete the .config file and run the application again to reset it. 

```
# API Keys #
TMDb = ""                                           <-- Define your api keys. Only TMDB is in use currently.
TVDb = ""
OMDb = ""


# Settings #
match_rate = ""                                     <-- Define a match rate, 1 being a perfect 100% match.
debug = True                                        <-- Display additional debug messages to the user.
keep_non_mkv = True                                 <-- Option to keep or skip non-mkv files. Will be reviewed later.
sorted_location = "***\Example"                     <-- Output directory for renaming files. Keep *** for relative outputs based on input directories, or define a custom directory (eg. C:/Example)
remove_covers = true extras                         <-- Enable deleting of mkv covers. Options: false, true, true extras (this being only for bonus content)
### Options for "non_video_files" --> sort/skip/delete/recycle (must be wrapped in quotes like "this")
non_video_files = "skip"                            <-- What you want to do with non-video files. Options: sort/skip/delete/recycle - note, delete not currently working.
bonus_folder_name = "Example"                       <-- Preferred bonus folder name eg. 'Bonus Content'
remove_mkv_titles = true                            <-- Option to modify mkv files to remove video track title.

# Keyword Settings #
stripped = true                                     <-- Remove specific keywords from files. Intended to remove specific names from extra content such as "x264" - Not currently in use.
keywords = ""                                       <-- The keywords to remove. Not currently in use.


# Rename Settings #
space_character = " "                               <-- Preferred space character. Can use whatever you want as a space, such as '.'
```