import arcpy
from arcpy import management as DM

tbl = "C:/WorkSpace/Phase5/Objects/Phase5_draft2.gdb/hexout1"
outpath = "C:/WorkSpace/Phase5/Objects"
dbfname = "hexout.dbf"
desc = arcpy.Describe(tbl)
fields = desc.fields
for field in fields:
	# print field.name[:5]
	calcfield = "[%s]" % field.name
	if (field.name[:5] == "VALUE"):
		newfname = "V" + field.name[6 - len(field.name):]
		print newfname
		print calcfield
		DM.AddField(tbl, newfname, "LONG")
		DM.CalculateField(tbl, newfname, calcfield, "VB", "")
		DM.DeleteField(tbl, field.name)
		arcpy.TableToTable_conversion(tbl, outpath, dbfname)
		