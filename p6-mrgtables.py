import csv
import os

leader = "D:\\Projects\\Texas Ecological Systems\\Phase VI\\SSURGOtables\\"
suffix = "\\tabular\\"
tables = ["comp", "cecoclas", "mapunit", "chorizon"]
counties = os.listdir(".")

for county in counties:
	if os.path.isdir(county):
		for table in tables:
			fname = county + suffix + table + ".txt"
			outfname = "p6_" + table + ".txt"
			source = open(fname, "r")
			destination = open(outfname, "a")
			for line in source: destination.write( line )
			source.close()
			destination.close()
