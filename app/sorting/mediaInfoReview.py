# -*- coding: utf-8 -*-

##########################################################################################################################
## Primarily used for grabbing and reviewing mediainfo data on a directed file. Returns specific media info parametors  ##
## 	that are of use to other areas of the application.																	##
##########################################################################################################################

# Required imports
import sys, subprocess, os
sys.path.insert(1, r'\app\scripts')
sys.path.insert(1, r'\app\api')
import utilities # pylint: disable=import-error


def get(path):											# Function to produce a mediainfo text output as a string (utf-8 format)
	# Relative dir path to binaries required
	dirname = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	mediainfoDir = dirname+"\\binaries\MediaInfo.exe"
	
	print(mediainfoDir)

	# Subprocess the mediainfo executable and retrieve the result as a string.
	proc = subprocess.Popen(mediainfoDir+' "{}"'.format(path), stdout=subprocess.PIPE)
	result = proc.stdout.read()
	
	# Return the result in ascii format
	return result.decode('utf-8')

# Return some basic media information (via MediaInfo) about a provided filepath. Output is height, scan type and codec (for now)
def basicInfo(path):
	height = scanType = codec = False				# Expected outputs
	videoInfo = audioInfo = subtitleInfo = False	# Expected split data - Initially set to False
	mediaInfoString = get(path)						# Request a complete MediaInfo string from the provided path

	# Attempt to split data to relevant variables. 
	try:
		videoInfo = mediaInfoString.split("\nVideo", 1)[1].split("\r\n\r", 1)[0]
	except:
		pass
	try:
		audioInfo = mediaInfoString.split("\nAudio", 1)[1].split("\r\n\r", 1)[0]
	except:
		pass
	try:
		subtitleInfo = mediaInfoString.split("\nText", 1)[1].split("\r\n\r", 1)[0]
	except:
		pass

	#################################################################################################
	# Assume we succeeded to split video data. Produce a standardized height from the height we find.
	try:
		h = int(videoInfo.split("\nHeight                                   : ", 1)[1].split("\n", 1)[0].replace(' ','').replace('pixels','')) # Full non-standardized resolution of the input file

		# Determine which range the collected height falls under.
		if 1440 < h <= 2160:
			height = 2160
		elif 1080 < h <= 1440:
			height = 1440
		elif 720 < h <= 1080:
			height = 1080
		elif 576 < h <= 720:
			height = 720
		elif 480 < h <= 576:
			height = 576
		elif 360 < h <= 480:
			height = 480
		else:
			height = 360
	except:
		print("Warning -- Resolution check failure")

	########################## 
	# Now let's focus on codec

	try:
		if "x264" in videoInfo.lower():
			codec = "x264"
		elif "avc" in videoInfo.lower():
			codec = "H.264"
		elif "x265" in videoInfo.lower():
			codec = "x265"
		elif "hevc" in videoInfo.lower():
			codec = "H.265"
		elif "vp9" in videoInfo.lower():
			codec = "VP9"
		else:
			print("Warning -- Not managing to find a matching codec from the mediainfo string.")
	except:
		print("Warning -- Codec check failure")

	########################################################
	# Now let's check if a scan type is defined in mediainfo
	try:
		if "Scan type                                :" in videoInfo:
			readScanType = videoInfo.split("\nScan type                                : ", 1)[1].split("\n", 1)[0]
			if "Progressive" in readScanType:
				scanType = "p"
			elif "Interlaced" in readScanType:
				scanType = "i"
			else:
				# Might need to revisit this later. For now, assuming interlaced if cannot find "progressive"
				scanType = "i"
		else:
			# Some codecs don't include this kind of data. Additional checks may be required.
			# Further improvements should be made here for additional codecs
			if codec is "x265" or codec is "H.265":
				scanType = "p"
	except:
		print("Warning -- Scan type check failure")
	
	

	# Finally, return the basic data. Some of this data might not be present though.
	return {'height': height, 'scanType': scanType, 'codec': codec}