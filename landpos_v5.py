# LANDPOS.AML translated to Python by Lee Elliott 12/5/2013
#  Calculates landposition based on the inverse distance weighted 
#  elevation of each cell in relation to its neighbors.  Determines 
#  mean elevation at various radii.  Subtracts model cell elevation 
#  from mean at each radius and divides by the distance.
#
#  Original Author:	Frank Biasi - The Nature Conservancy 
#  Original Date: 	6/14/2000
#
#  Arguments:  .dem = name of study area dem grid
#		.num = number of cells for search radius
#
#  Output grid:   landpos 
# -------------------------------------------------------------------------------

import sys
import os
from arcpy import management as DM
import arcpy
from arcpy.sa import *
arcpy.env.workspace = os.getcwd()
from time import time
from string import zfill
from datetime import date

gap = 1
start = 1

class LicenseError(Exception):
    pass
try:
    if arcpy.CheckExtension("Spatial") == "Available":
        arcpy.CheckOutExtension("Spatial")
        print "Spatial Analyst license is AVAILABLE"
    else:
        # raise a custom exception
        #
        raise LicenseError
except LicenseError:
    print "Spatial Analyst license is unavailable"
except:
    print arcpy.GetMessages(2)
def elapsed_time(t0):
	seconds = int(round(time() - t0))
	h,rsecs = divmod(seconds,3600)
	m,s = divmod(rsecs,60)
	return zfill(h,2) + ":" + zfill(m,2) + ":" + zfill(s,2)
	
if len(sys.argv) < 3:
	print "**********************************************************"
	print "Usage: landpos.py <dem> <search_radius_in_number_of_cells>"
	print "Enter parameters below."
	print "**********************************************************"
	demname = raw_input("Enter name of DEM file: ")
	num = int(raw_input("Enter search radius in number of cells: "))
else:
	demname = sys.argv[1]
	num = int(sys.argv[2])
if not(arcpy.Exists(demname)): 
	print "**********************"
	print "*DEM FILE NOT PRESENT*"
	print "**********************"
	quit()
	
landposname = "landpos"
if arcpy.Exists(landposname): 
	newname = raw_input("File \"landpos\" exists!\nEnter different name, or return to overwrite: ")
	if newname == "":
		print "File \"landpos\" will be OVERWRITTEN."
		DM.Delete("landpos")
	else: landposname = newname

cellsize = DM.GetRasterProperties(demname, "CELLSIZEX").getOutput(0)
print "Using dem = " + demname + " and search radius = " + str(num) + " for cellsize = " + str(cellsize) + "."

processstart = time()
i = 1
print "Annulus at " + str(start) + " cells running"
elev = Divide(Minus(FocalStatistics(demname,NbrAnnulus(start - 1, start, "CELL"), "MEAN", "NODATA"), arcpy.sa.Float(Raster(demname))), (float(start) * float(cellsize)))
for j in range(start + gap, num + 1, gap):
        print "Annulus at " + str(j) + " cells running"
        i += 1
        elev = Plus(elev, Divide(Minus(FocalStatistics(demname,NbrAnnulus(j - 1, j, "CELL"), "MEAN", "NODATA"), arcpy.sa.Float(Raster(demname))), (float(j) * float(cellsize))))
Divide(elev, float(i)).save(landposname)
print "Elapsed time: " + elapsed_time(processstart)
