# Python script to read gpx file and output name, time, latitude and longitude from waypoints.
# Lee Elliott 13 mar 2013

import re
basefilename = "Waypoints_08-JUN-12."
infilename = basefilename + "gpx"
outfilename = basefilename + "csv"
print infilename
infile = open(infilename, "r")
outfile = open(outfilename, "a")
ptlines = []
regex = re.compile(r'<wpt (.+?)</wpt>')
regex2 = re.compile(r'^lat="([0-9\.\-]+)" lon="(\S+)".+<time>(.+)</time><name>(.+)</name')
outfile.write("\"id\", \"time\", \"lat\", \"long\"\n")
while 1:
	line = infile.readline()
	if not line: break
	ptlines = regex.findall(line)
	for item in ptlines:
		m1 = regex2.search(item)
		print item
		if m1:
			outstr = "\"%s\", \"%s\", %s, %s\n" % (m1.group(4), m1.group(3), m1.group(1), m1.group(2))
			outfile.write(outstr)
infile.close()
outfile.close()