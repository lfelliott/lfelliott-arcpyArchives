import csv
import re

source = open("esp_names_tab.txt", "r")
outfile = open("esp_out.txt", "a")
p = re.compile(r'\s+(\d+)')
for line in source:
	outline = line.replace("\t", "|")
	# outfile.write(outline)
	itr = p.finditer(outline)
	for i in itr:
		outline = outline.replace(i.group(), "\n" + i.group())
outfile.write(outline)

	
	