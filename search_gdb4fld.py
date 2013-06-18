import arcpy
from arcpy import management as DM

searchstr = "LocType"
searchfldr = "e:/TexasEcologicalSystemsArchive/Range_Maps"
arcpy.env.workspace = searchfldr
gdbs = arcpy.ListFiles("*.gdb")
print(searchstr)
for gdb in (gdbs):
	print("\t" + gdb)
	wrkspace = "%s/%s" % (searchfldr, gdb)
	arcpy.env.workspace = wrkspace
	fcs = arcpy.ListFeatureClasses("*")
	for fc in (fcs):
		fields = arcpy.ListFields(fc)
		for field in fields:
			if (field.name == searchstr):
				print("\t\t" + fc)
	tbls = arcpy.ListTables()
	for tbl in (tbls):
		fields = arcpy.ListFields(fc)
		for field in fields:
			if (field.name == searchstr):
				print("\t\t" + tbl)
