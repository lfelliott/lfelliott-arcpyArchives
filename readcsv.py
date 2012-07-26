import csv
selectstring = "\"ECOCLASSNA\" = 'Gravelly, Hot Desert Shrub' and \"slope20\" = 0"
rows = csv.reader(open('P5Key.csv', 'rb'), delimiter = ',', quotechar='"')
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
		selectstr = selectstr + " AND \"slope\" > " + gt_slope
	if (lt_slope):
		selectstr = selectstr + " AND \"slope\" <= " + lt_slope
	if (gt_insol):
		selectstr = selectstr + " AND \"insol\" > " + gt_insol
	if (lt_insol):
		selectstr = selectstr + " AND \"insol\" <= " + lt_insol
	print selectstr
