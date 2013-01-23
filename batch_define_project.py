# Code from Michael Diener
# http://spatialmounty.blogspot.com/2012/08/how-to-batch-define-projections-with.html

import arcpy
from arcpy import env
import os
env.workspace = "D:\\GIS\\Texas\\CLUData\\TX_FSA_CLU_asof_April1_2006\\UTM13"
fcs = arcpy.ListFeatureClasses('*')
try:
	for file in fcs:
		inData = file
		# need to esacape all the " in the PROJCS string
		coordinateSystem = "PROJCS[\"NAD_1983_UTM_Zone_13N\",GEOGCS[\"GCS_North_American_1983\",DATUM[\"D_North_American_1983\",SPHEROID[\"GRS_1980\",6378137.0,298.257222101]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Transverse_Mercator\"],PARAMETER[\"False_Easting\",500000.0],PARAMETER[\"False_Northing\",0.0],PARAMETER[\"Central_Meridian\",-105.0],PARAMETER[\"Scale_Factor\",0.9996],PARAMETER[\"Latitude_Of_Origin\",0.0],UNIT[\"Meter\",1.0]]"
		arcpy.DefineProjection_management(inData, coordinateSystem)
except arcpy.ExecuteError:
	print arcpy.GetMessages(2)
	arcpy.AddError(arcpy.GetMessages(2))
except Exception as e:
	print e.args[0]
	arcpy.AddError(e.args[0])
