import arcpy
from arcpy import management as DM


#arcpy.env.workspace = "e:/TexasEcologicalSystemsArchive/Range_Maps/FerruginousHawk.gdb"
arcpy.env.workspace = "e:/TexasEcologicalSystemsArchive/Range_Maps"
searchstr = "LocType"

datasets = arcpy.ListFiles("*.gdb")
for dataset in datasets:
	print(dataset)