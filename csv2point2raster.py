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
	
currentdir = os.getcwd()
#arcpy.env.workspace = "test.gdb"
searchstr = re.compile(r'(.+)?\.csv$')
filelist = []

for filename in os.listdir(currentdir):
	m1 = searchstr.match(filename)
	if m1:
		csv_input = filename
		filelist.append(filename)

UTM12N_PROJ = "PROJCS['NAD_1983_UTM_Zone_12N',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-111.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]"


for fname in filelist:
	starttime = time()
	print fname
	csv_input = fname
	temp_layer = fname[:-4]
	gdb_output = "LandFacets.gdb/%s" % temp_layer
	raster_file = "%s\\Raster\\%s_rast" % (currentdir, temp_layer)
	arcpy.MakeXYEventLayer_management(csv_input,"utm_n","utm_e", temp_layer, UTM12N_PROJ)
	print "...xy event layer made"
	arcpy.CopyFeatures_management(temp_layer, gdb_output)
	print "...copied to gdb"
	arcpy.Delete_management(temp_layer)
	print "...temp layer deleted"
	arcpy.PointToRaster_conversion(gdb_output, "cluster", raster_file, "MOST_FREQUENT", "NONE", "30")
	print "...raster made"
	print "process time = " + elapsed_time(starttime)