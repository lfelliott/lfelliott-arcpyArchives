import arcpy
import os
import re
from time import time
from string import zfill
from datetime import date

def elapsed_time(t0):
	seconds = int(round(time() - t0))
	h,rsecs = divmod(seconds,3600)
	m,s = divmod(rsecs,60)
	return zfill(h,2) + ":" + zfill(m,2) + ":" + zfill(s,2)
overallstart = time()
	
currentdir = os.getcwd()
rasterdir = currentdir + "\\Raster"
mergedrastername = "landfacet.img"
searchstr = re.compile(r'(.+)?\.csv$')
filelist = []

for filename in os.listdir(currentdir):
	m1 = searchstr.match(filename)
	if m1:
		csv_input = filename
		filelist.append(filename)

UTM12N_PROJ = "PROJCS['NAD_1983_UTM_Zone_12N',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-111.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]"
# UTM12N_PRJ = 'PROJCS["NAD_1983_UTM_Zone_12N",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",-111.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]'
for fname in filelist:
	starttime = time()
	print fname
	csv_input = fname
	temp_layer = fname[:-4]
	gdb_output = "LandFacets.gdb/%s" % temp_layer
	raster_file = "%s\\Raster\\%s_rast" % (currentdir, temp_layer)
	arcpy.MakeXYEventLayer_management(csv_input,"utm_e","utm_n", temp_layer, UTM12N_PROJ)
	print "...xy event layer made"
	arcpy.CopyFeatures_management(temp_layer, gdb_output)
	print "...copied to gdb"
	arcpy.Delete_management(temp_layer)
	print "...temp layer deleted"
	arcpy.AddField_management(gdb_output, "landfacet", "LONG")
	print "...added landfacet field"
	arcpy.CalculateField_management(gdb_output, "landfacet", "([glgysbstrt]* 10) + [cluster]", "VB", "")
	print "...calculated landfacet field from geo*10+cluster"
	arcpy.PointToRaster_conversion(gdb_output, "landfacet", raster_file, "MOST_FREQUENT", "NONE", "30")
	print "...raster made"
	print "process time = " + elapsed_time(starttime)
arcpy.MosaicToNewRaster_management("'Raster\\bmc_rast';'Raster\\clm_rast';'Raster\\eos_rast';'Raster\\gslunk_rast';'Raster\\qoa_rast';'Raster\\qya_rast';'Raster\\shl_rast';'Raster\\slm_rast';'Raster\\snd_rast'", rasterdir, mergedrastername, UTM12N_PROJ, "8_BIT_UNSIGNED", "30", "1", "LAST", "FIRST")
print "Rasters merged"
print "OVERALL ELAPSED: " + elapsed_time(overallstart)