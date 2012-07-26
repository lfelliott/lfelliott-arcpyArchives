import csv

fcs = ["test"]
for fc in fcs:
	print fc
	layername = "l_" + fc
	print layername
	calcfield = "\"%s.VegNum\"" % fc
	print calcfield
selectstrs = []
rows = csv.reader(open('p5cmplx.csv', 'rb'), delimiter = ',', quotechar='"')
for row in rows:
	ecogrp = row[0]
	landcover = row[1]
	vegtype = row[2]
	gt_elev = row[3]
	lt_elev = row[4]
	gt_slope = row[5]
	lt_slope = row[6]
	gt_insol = row[7]
	lt_insol = row[8]
	selectstr = "\"EcoGroup\" = '%s' AND \"lulc\" = %s" % (ecogrp, landcover)
	if (gt_elev):
		selectstr = selectstr + " AND \"elev\" > " + gt_elev
	if (lt_elev):
		selectstr = selectstr + " AND \"elev\" <= " + lt_elev
	if (gt_slope):
		selectstr = selectstr + " AND \"slp\" > " + gt_slope
	if (lt_slope):
		selectstr = selectstr + " AND \"slp\" <= " + lt_slope
	if (gt_insol):
		selectstr = selectstr + " AND \"insol\" > " + gt_insol
	if (lt_insol):
		selectstr = selectstr + " AND \"insol\" <= " + lt_insol
	selectstrs.append(selectstr)

for selectstr in selectstrs:
	print ""
print selectstr
for selectstr in selectstrs:
	print selectstr
	