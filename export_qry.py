import csv
outf = open("c:/workspace/phase5/Objects/qrystr.txt", "a")

outf.writelines("\n--Phase 5 --\n")
rows = csv.reader(open('slpegrp.csv', 'rb'), delimiter = ',', quotechar='"')
selectstr = ""
for row in rows:
	ecogrp = row[0]
	selectstr = selectstr + "\"EcoGroup\" = '%s' OR "  % ecogrp
	print selectstr
outf.writelines(selectstr)