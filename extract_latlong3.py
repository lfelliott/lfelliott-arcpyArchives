# Extract latitude and longitude from exif and export as a csv with filename, latitude, longitude
# Script must reside in same directory as images (as the script is now written)
# Lee Elliott 20120824
# Modified from erans script at https://gist.github.com/983821
# Moved opening image to get_exif_data so parameter passed to that function is now the file name, also implemented recommendation from brendn



from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
import string
import re

def get_exif_data(image):
	# Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags
	exif_data = {}
	img = Image.open(image)
	info = getattr(img, '_getexif', lambda: None)()
	if info:
		for tag, value in info.items():
			decoded = TAGS.get(tag, tag)
			if decoded == "GPSInfo":
				gps_data = {}
				for t in value:
					sub_decoded = GPSTAGS.get(t, t)
					gps_data[sub_decoded] = value[t]

				exif_data[decoded] = gps_data
			else:
				exif_data[decoded] = value
	return exif_data

def _get_if_exist(data, key):
    if key in data:
        return data[key]

    return None

def _convert_to_degress(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)

def get_lat_lon(exif_data):
	lat = 0
	lon = 0
#	"""Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
	if "GPSInfo" in exif_data:
		gps_info = exif_data["GPSInfo"]
		gps_latitude = _get_if_exist(gps_info, "GPSLatitude")
		gps_latitude_ref = _get_if_exist(gps_info, 'GPSLatitudeRef')
		gps_longitude = _get_if_exist(gps_info, 'GPSLongitude')
		gps_longitude_ref = _get_if_exist(gps_info, 'GPSLongitudeRef')
		if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
			lat = _convert_to_degress(gps_latitude)
			if gps_latitude_ref != "N":
				lat = 0 - lat
			lon = _convert_to_degress(gps_longitude)
			if gps_longitude_ref != "E":
				lon = 0 - lon
		llstr_tmp = lat, lon
	return lat, lon


if __name__ == "__main__":
	walk = 1
	filelist = []
	startpath = 'd:\\Data\\Images'
	if (walk):
		for root, dirs, files in os.walk(startpath):
			for name in files:
				if (name[-3:].upper() == "JPG"):
					filelist.append(root + "\\" + name)
	else:
		for filename in os.listdir("."):
			if (filename[-3:].upper() == "JPG"):
				filelist.append(filename)
	outfile = open("photolist_full.csv", "a")
	outfile.write("\"Species\",\"Filename\", lat, long\n")
	p1 = re.compile(r'.+\\(.+?)-[A-Z]')
	for image in filelist:
		exif_data = {}
		m1 = p1.search(image)
		species = "None"
		if m1:
			species = m1.group(1)
		try:
			exif_data = get_exif_data(image)
#			print("exif_data retrieved")
		except IOError as e:
			print "I/O error({0}): {1}".format(e.errno, e.strerror)
			print image
		except ValueError:
			print "Could not convert data to an integer."
		except:
			print "Unexpected error:", sys.exc_info()[0]
		if "GPSInfo" in exif_data:
			llstr = get_lat_lon(exif_data)
			if (llstr[0] > 0):
				outputstr = "\"%s\",\"%s\",%f,%f\n" % (species, image, llstr[0], llstr[1]) 
				outfile.write(outputstr)
	outfile.close()
