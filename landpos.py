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
cellsizeres = DM.GetRasterProperties(demname, "CELLSIZEX")
cellsize = cellsizeres.getOutput(0)
print "Using dem = " + demname + " and search radius = " + str(num) + " for cellsize = " + str(cellsize) + "."
landpos_divisor = num / gap
for j in range(start,num + 1, gap):
	print "annulus at " + str(j) + " cells"
	# Uncomment below line to allow annulus to be great than 1 cell
	# annulus_widgth = gap - 1
	annulus_width = 0
	focalmean = FocalStatistics(demname,NbrAnnulus(j, j + annulus_width, "CELL"), "MEAN", "NODATA")
	tempres = Minus(arcpy.sa.Float(focalmean), arcpy.sa.Float(Raster(demname)))
	weight = float(j) * float(cellsize)
	elevres = Divide(arcpy.sa.Float(tempres), weight)
	if j == start: elev = elevres
	else: elev = Plus(elev, elevres)
landpos = Divide(elev, float(num))
landposname = "landpos"
if arcpy.Exists(landposname): 
	newname = raw_input("File \"landpos\" exists!\nEnter different name, or return to overwrite: ")
	if newname == "":
		print "File \"landpos\" will be OVERWRITTEN."
		DM.Delete("landpos")
	else: landposname = newname
landpos.save(landposname)