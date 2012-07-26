fcs = ["p5_north_working", "p5_south_working"]
suffix = "02"
for fc in fcs:
	print fc
	print "\"%s.lulc\" = %s" % (fc, suffix)

newlist = []
f = open('ecogrps.csv')
for item in f.readlines():
	newlist.append(item.strip())
for item in newlist:
	prtstr = "\"EcoGroup\" = '%s'" % item
	print prtstr
print newlist[0]