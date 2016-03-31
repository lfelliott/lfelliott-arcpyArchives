import arcpy
from arcpy import management as DM
from decimal import *
from time import time
from string import zfill
from datetime import date
arcpy.env.workspace = 'f:/projects/ewg/Nugget40_IL/IL40_Compiled.gdb/'
# test case
#arcpy.env.workspace = 'f:/projects/ewg/Nugget40_IL/test.gdb/'
fcs = arcpy.ListFeatureClasses("*")
layer = 'layername'
fldname = "temp"
tempfld = "\"[temp]\""
precision = 18
scale = 11
skipflds = ['OBJECTID', 'Shape', 'GLC_a2', 'GLC_h', 'GLC_m', 'GLD_a2', 'class', 'prec', 'Shape_Length', 'Shape_Area']
selectstr = "\"Mn_l1\" = '0' and \"Mn_l2\" = '0' and \"Mn_l3\" = '0'"

def elapsed_time(t0):
	seconds = int(round(time() - t0))
	h,rsecs = divmod(seconds,3600)
	m,s = divmod(rsecs,60)
	return zfill(h,2) + ":" + zfill(m,2) + ":" + zfill(s,2)

def isfloat(value):
	try:
		float(value)
		return True
	except:
		return False
def fieldExists(fc, field):
	fl = arcpy.ListFields(fc)
	result = False
	for f in fl:
		if f.name == field:
			 result = True
	return result

starttime = time()
for fc in fcs:
	fieldns = []
	print elapsed_time(starttime)
	print fc
	DM.MakeFeatureLayer(fc, layer)
	DM.SelectLayerByAttribute(layer, "NEW_SELECTION", selectstr)
	count = int(DM.GetCount(layer).getOutput(0))
	if count > 0:
		DM.DeleteFeatures(layer)
		print "%d objects deleted." % count
	DM.SelectLayerByAttribute(layer, "CLEAR_SELECTION", selectstr)
	if not(fieldExists(fc, fldname)):
		DM.AddField(layer, fldname, "DOUBLE") 
	fieldList = arcpy.ListFields(fc)
	DM.CalculateField(layer, fldname, 0)
	for field in fieldList:
		fieldns.append(field.name)
# test case
#	fieldns = ['Sd_l8', 'Sd_l6']
	for field in fieldns:
		cursor = arcpy.UpdateCursor(fc)
#		print field
		if not(field in skipflds):
			for row in cursor:
				dblval = 0
				strval = row.getValue(field)
				dblval = float(strval)
#				print dblval
				if (isfloat(dblval)): 
					row.setValue(fldname, dblval)
					cursor.updateRow(row)
			DM.DeleteField(layer, field)
			DM.AddField(layer, field, "DOUBLE")
			DM.CalculateField(layer, field, "[temp]")
	DM.DeleteField(layer, fldname)
	DM.Delete(layer)		
print elapsed_time(starttime)