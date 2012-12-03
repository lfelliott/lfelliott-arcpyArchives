import arcpy
arcpy.env.workspace = "D:/Projects/Texas Ecological Systems/TPWD Public FTP/dropboxV/TexasVegMap.gdb"
fcs = arcpy.ListFeatureClasses("*")
for fc in (fcs):
	print fc