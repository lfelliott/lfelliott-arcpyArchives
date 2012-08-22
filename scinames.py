import csv
import re

source = open("scinames.txt", "r")

outfile = open("scinamelist2.txt", "a")
outlines = []
for line in source:
	line2 = line[:-1]
	species = line2 + " <(.+?)>"
	#print line2
	p1 = re.compile(species)
	source2 = open("descript2.txt", "r")
	
	for paragraph in source2:
		m1 = p1.search(paragraph)
		if (m1 != None):
			cname = m1.group(1)
			#print species
			#print line2
			#print cname
			outline = line2 + "|" + cname + "\n"Init
			outfile.write(outline)
	source2.close()
source.close()
outfile.close()

		