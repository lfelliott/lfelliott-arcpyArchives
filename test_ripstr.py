import csv
riprows = csv.reader(open('riparian.csv', 'rb'), delimiter = ',', quotechar='"')
selectstrs = []
weststrs = []
southstrs = []
selectdict =  {}
for row in riprows:
	floodpl = row[0]
	landcover = row[1]
	vegtype = row[2]
	gt_elev = row[3]
	lt_elev = row[4]
	selectstr = "\"floodpl\" = '%s' AND \"riparian24\" = 1 AND \"lulc\" = %s" % (floodpl, landcover)
	if (gt_elev):
		selectstr = selectstr + " AND \"elev\" > " + gt_elev
	if (lt_elev):
		selectstr = selectstr + " AND \"elev\" <= " + lt_elev
	selectdict[selectstr] = vegtype
	selectstrs.append(selectstr)
	if (floodpl == "CH"):
		weststrs.append(selectstr)
		southstrs.append(selectstr)
	if (floodpl == "SP"):
		southstrs.append(selectstr)
for selectstr in selectstrs:
	print selectstr
print "\nWest Strings\n"
for thing in weststrs:
	print thing + ": " + selectdict[thing]
print "\nSouth Strings\n"
for thing in southstrs:
	print thing + ": " + selectdict[thing]
