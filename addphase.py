import arcpy
import re
from arcpy import management as DM
arcpy.env.workspace = "D:/Projects/Texas Ecological Systems/TPWD Public FTP/dropboxV/TexasVegMap.gdb"
fcs = arcpy.ListFeatureClasses("*")
#fcs = ("Phase5_North_Objects", "Phase5_West_Objects", "Phase4_South_Objects")

for fc in (fcs):
	m = re.search(r'Phase(\d).+_dslv', fc)
	if m:
		phase = m.group(1)
		print fc
		print phase
		DM.CalculateField(fc, "Phase", phase, "VB", "")
		
	#DM.Dissolve(fc, fcdslv, "Veg_ID", "", "SINGLE_PART", "DISSOLVE_LINES")