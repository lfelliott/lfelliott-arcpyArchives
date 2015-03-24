import arcpy
from arcpy import management as DM
from time import time
from string import zfill
from datetime import date

def elapsed_time(t0):
	seconds = int(round(time() - t0))
	h,rsecs = divmod(seconds,3600)
	m,s = divmod(rsecs,60)
	return zfill(h,2) + ":" + zfill(m,2) + ":" + zfill(s,2)

def replace_field(layer, oldname, newname):
	expression1 = "[" + oldname + "]"
	DM.CalculateField(layer, newname, expression1, "VB")
	DM.DeleteField(layer, oldname)
	
# Location of geodatabase for the featureclasses to which changes will be applied	
arcpy.env.workspace = "c:/Workspace/TexasEnduringFeatures.gdb/"
# List of feature classes in geodatabases to which changes will be applied
# List of fields that need to be in the final featureclass
baseflds = ['epa_ecoreg', 'slope', 'slope40', 'cliff', 'riparian', 'land_pos', 'ridge', 'ravine', 'Ecoclass_ID', 'Econame', 'basin', 'EcoGroup', 'ef', 'ef_name']
# Dictionary of field types for the list of fields for the final featureclass
fldtypes = {'epa_ecoreg' : 'TEXT', 'slope' : 'SHORT', 'slope40' : 'SHORT', 'cliff' : 'SHORT', 'riparian' : 'SHORT', 'land_pos' : 'SHORT', 'ridge' : 'SHORT', 'ravine' : 'SHORT', 'Ecoclass_ID' : 'TEXT', 'Econame' : 'TEXT', 'basin' : 'TEXT', 'EcoGroup' : 'TEXT', 'ef' : 'LONG', 'ef_name' : 'TEXT'}
# Dictionary of field length for TEXT fields for final featureclass
fldlength = {'epa_ecoreg' : 5, 'Ecoclass_ID' : 20, 'Econame' : 50, 'basin' : 50, 'EcoGroup' : 150, 'ef_name' : 150}
	
layername = "ef_layer"
def add_flds(fc):
	DM.MakeFeatureLayer(fc, layername)
	fldlst = arcpy.ListFields(layername)
	fc_dslv = fc + "_dslv"
	fldnames = []
	for fld in fldlst:
		fldnames.append(fld.name.upper())
	for basefld in baseflds:
		if (fldnames.count(basefld.upper()) == 0): 
			if (fldtypes[basefld] == "TEXT"): DM.AddField(layername, basefld, "TEXT", "", "", fldlength[basefld])
			else: DM.AddField(layername, basefld, fldtypes[basefld])
			if "EcoclassID" in fldnames: replace_field(layername, "EcoclassID", "Ecoclass_ID")
# Set of if statements to copy data from original fields to final fields, this requires knowing what original fields correspond to final fields. 
# These equivalencies assume the same field types for the fields in the original fields vs the final fields
	if "slope20" in fldnames: replace_field(layername, "slope20", "slope")
	if "slope100" in fldnames: replace_field(layername, "slope100", "cliff")
	if "ecogrp2" in fldnames: replace_field(layername, "ecogrp2", "EcoGroup")
	if "riparian24" in fldnames: replace_field(layername, "riparian24", "riparian")
	if "riperian24" in fldnames: replace_field(layername, "riperian24", "riparian")
	if "ECOCLASSNA" in fldnames: replace_field(layername, "ECOCLASSNA", "Econame")
	if "floodpl" in fldnames: replace_field(layername, "floodpl", "basin")
	if "sm_stream" in fldnames: replace_field(layername, "sm_stream", "riparian")
	if "enduring_feature" in fldnames: replace_field(layername, "enduring_feature", "ef")
	sourcefieldstr = fc + ".ef_name"
	print "   adding ef_name...."
	DM.AddJoin(layername, "ef", "m:/TX_EnduringFeatures/EFS.DBF", "EF", "KEEP_COMMON")
	DM.CalculateField(layername, sourcefieldstr, "[EFS.EF_NAME]", "VB")
	DM.RemoveJoin(layername, "EFS")
	DM.Delete(layername)


for fcname in fcs:
		print fcname
		processstart = time()
		add_flds(fcname)
		print "Elapsed time: " + elapsed_time(processstart)
