import arcpy
from arcpy import management as DM
arcpy.env.workspace = 'F:/projects/ewg/Nugget40_IL/'
fcs = arcpy.ListFeatureClasses("*")
tgtprefix = 'm:/ewg/il_dissolves.gdb/'
for fc in fcs:
	tileno = fc[-7:-4]
	tgtfc = "%st%s" % (tgtprefix, tileno)
	print tgtfc
	DM.Dissolve(fc, tgtfc, "", "", "MULTI_PART", "DISSOLVE_LINES")
	print "   done"