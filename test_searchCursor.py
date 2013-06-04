import arcpy
from arcpy import env

env.workspace = "d:\\gis\\gme"
fc = "outpts.shp"
fields = ["SETID"]
cur = arcpy.SearchCursor(fc)
maxid = 0
for row in cur:
	if (row.SETID > maxid):
		maxid = row.SETID
print maxid