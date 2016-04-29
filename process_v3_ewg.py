# Functions for processing tiles of objects. These functions were developed during the East West Gateway project.
# 1)  list_full_fcs(workspace) - returns a list of all the feature classes in the workspace (including in subdirectories) with path
#	parameters-workspace=folder that incudes shapefiles and subdirectories.
#	returns - list of feature classes
# 2)  list filename_fcs(workspace) - returns list of feature classes in workspace without the path
#	parameters-workspace=folder that incudes shapefiles and subdirectories.
#	returns - list of feature classes
# 3)  rename_files(wsroot) - renames tiles to shorter name based on tile number
# 4)  kill_zeroes(fc) - deletes features from a feature class that has 3 bands from 2 images = 0, deletes the feature class if all 0s
# 5)  add_class_field(fc) -	adds the field "class", a short integer if it's not already in the feature class
# 6)  make_empty_file(fc, newfile) - make an empty feature class (newfile) with the same structure as another (fc)
# 7)  add_class_within_dslv(fc, dslvfc, outputfc) - for getting classed polygons out of full set of features using dissolved data. We use this function
#    to retrieve a set of new objects from a set of dissolved samples from older objects. Old objects were dissolved on class. Class is added to new objects and
#    all the new objects that are completely within the older dissolved projects are exported with the class from the old objects.
# 8)  add_negclass_centroids(fc, pointfc, outputfc) - takes centroids of old objects and selects features from the new objects and exports the selection with the class
#    from the old objects. The class is assigned as the negative of the original class because these objects will need to be reviewed.
# 9)  get_aa_sampleobjs(fc, aapts, outaa) - exports features from the feature class that intersects the aa points and assigns the class from the aa points. The new features will 
#    need to be reviewed.
# 10) add_shape_area(fc) - adds the field shape_area and calculates the area for a feature class
# 11) make_tile_index(workspace) - makes a set of tiles for all the tiles in workspace and copies it to a subdirectory of workspace named "empty". Names need to be applied in a 
#   separate function. Then they can be merged into a single.
# 12) add_tile_label(workspace) - gets the tile number from the file name and adds it as a label to the files

# Function returns list of the feature classes with full path
def list_full_fcs(workspace):
	fcs = []
	walk = arcpy.da.Walk(workspace, datatype = "FeatureClass", type="Polygon")
	for dirpath, dirnames, filenames in walk:
		for filename in filenames:
			fcs.append(os.path.join(dirpath, filename))
	return fcs

# Function returns list of feautre class names (shp extension included)	
def list_filename_fcs(workspace):
	fnames = []
	walk = arcpy.da.Walk(workspace, datatype = "FeatureClass", type="Polygon")
	for dirpath, dirnames, filenames in walk:
		for filename in filenames:
			fnames.append(filename)
	return fnames

# Function renames files in all subdirectories of w	
def rename_files(wsroot):
	fullnames = []
	filenames = []
	p1str = '%s\\Nugget(\d+)\\' % wsroot
	p1 = re.compile(r'\\Nugget(\d+\S{0,3})\\')
	p2 = re.compile(r'tiles.tile(\d{1,4})\.')
	for root, dirs, files in os.walk(wsroot):
		for name in files:
			fullnames.append(os.path.join(root,name))
			filenames.append(name)
	for name in fullnames:
		m1 = p1.search(name)
		m2 = p2.search(name)
		ext = name[-3:]
		nugnum = m1.group(1)
#		newname = '%s\\Nugget%s\\Nug%s_tile%s.%s' % (wsroot,m1.group(1), m1.group(1), m2.group(1), ext)
		newname = '%s\\Nug%s_tile%s.%s' % (wsroot,m1.group(1), m2.group(1), ext)
		print "%s -> %s" % (name, newname)
		os.rename(name, newname)

# Function deletes feature classes that have nothing but zeroes in 3 bands of both dates and deletes features with zeros		
def kill_zeroes(fc):
	layer = 'layername'
	DM.MakeFeatureLayer(fc, layer)
	DM.SelectLayerByAttribute(layer, "SWITCH_SELECTION")
	recs = int(DM.GetCount(layer).getOutput(0))
	selectstr = "(\"Mn_l1\" = 0 and \"Mn_l2\" = 0 and \"Mn_l3\" = 0) or (\"Mn_l5\" = 0 and \"Mn_l6\" = 0 and \"Mn_l7\" = 0)"
	DM.SelectLayerByAttribute(layer, "NEW_SELECTION", selectstr)
	count = int(DM.GetCount(layer).getOutput(0))
	if count > 0:
		if recs == count:
			DM.Delete(layer)
			DM.Delete(fc)
		else:
			DM.DeleteFeatures(layer)
	DM.Delete(layer)
			
# Function to add field class
def add_class_field(fc):			
	fields = arcpy.ListFields(fc)
	temp = []
	for field in fields:
		temp.append(field.name)
	if not ("class" in temp):
		DM.AddField(fc, "class", "SHORT")
		
# Function to make an empty file with the structure of the object file.
def make_empty_file(fc, newfile):
	path, newfilename = os.path.split(newfile)
	if not (os.path.isfile(newfile)):
		geometry_type = "POLYGON"
		has_m = "DISABLED"
		has_z = "DISABLED"
		spatial_reference = arcpy.Describe(fc).spatialReference
		print "MAKING NEW OUTPUT FILE!!!"
		arcpy.CreateFeatureclass_management(path, newfilename, geometry_type, fc, has_m, has_z, spatial_reference)

# Adds class field using function above and changes class to class of dissolved		
def add_class_within_dslv(fc, dslvfc, outputfc):
	classes = [1,2,3,4,5,6,7]
	add_class_field(fc)
	layer = 'layername'
	dslvlyr = 'dslvlyr'
	outlyr = 'outlyr'
	DM.MakeFeatureLayer(fc, layer)
	DM.MakeFeatureLayer(dslvfc, dslvlyr)
	make_empty_file(fc, outputfc)
	for fld_class in classes:
		selectstr = '\"class\" = %d' % fld_class
		DM.SelectLayerByAttribute(dslvlyr, "NEW_SELECTION", selectstr)
		count = int(DM.GetCount(dslvlyr).getOutput(0))
		if count > 0:
#			print('%d dissolved objects selected for class %d' % (count, fld_class))
			DM.SelectLayerByLocation(layer, "COMPLETELY_WITHIN", dslvlyr, "", "NEW_SELECTION")
			count2 = int(DM.GetCount(layer).getOutput(0))
			if count2 > 0:
#				print('%d objects selected for class %d' % (count2,fld_class))
				DM.CalculateField(layer, "class", fld_class)
				DM.Append(layer, outputfc, "NO_TEST", "", "")
	DM.Delete(layer)
	DM.Delete(dslvlyr)

# Changes field class to negative of class in points from centroids of old samples (to be run after add_class_within_dslv)	
def add_negclass_centroids(fc, pointfc, outputfc):
	classes = [1,2,3,4,5,6,7]
	add_class_field(fc)
	layer = 'layername'
	centlyr = 'centroid_layer'
	DM.MakeFeatureLayer(fc, layer)
	DM.MakeFeatureLayer(pointfc, centlyr)
	make_empty_file(fc, outputfc)
	for fld_class in classes:
		negclass = -(fld_class)
		selectstr = "\"class\" = 0 or \"class\" is null"
		DM.SelectLayerByAttribute(layer, "NEW_SELECTION", selectstr)
		count1 = int(DM.GetCount(layer).getOutput(0))
#		print('%d objects do not have class assigned' % count1)
		selectstr = "\"class\" = %d" % fld_class
		DM.SelectLayerByAttribute(centlyr, "NEW_SELECTION", selectstr)
		count2 = int(DM.GetCount(centlyr).getOutput(0))
#		print('%d object centroids in class %d' % (count2,fld_class))
		if (count1 > 0 and count2 > 0):
			DM.SelectLayerByLocation(layer, "INTERSECT", centlyr,"", "SUBSET_SELECTION")
			count3 = int(DM.GetCount(layer).getOutput(0))
			if count3 > 0:
#				print('%d objects of class %d selected' % (count3, fld_class))
				DM.CalculateField(layer, "class", negclass)
				DM.Append(layer, outputfc, "NO_TEST", "", "")
	DM.Delete(layer)
	DM.Delete(centlyr)

def get_aa_sampleobjs(fc, aapts, outaa):
	classes = [1,2,3,4,5,6,7]
	add_class_field(fc)
	layer = 'layername'
	aalyr = 'aa_layer'
	outlyr = 'out_layer'
	DM.MakeFeatureLayer(fc, layer)
	DM.MakeFeatureLayer(aapts, aalyr)
	make_empty_file(fc, outaa)
	for fld_class in classes:
		selectstr = "\"CID\" = %d" % fld_class
		DM.SelectLayerByAttribute(aalyr, "NEW_SELECTION", selectstr)
		count1 = int(DM.GetCount(aalyr).getOutput(0))
		if (count1 > 0):
			DM.SelectLayerByLocation(layer, "INTERSECT", aalyr,"", "NEW_SELECTION")
			count2 = int(DM.GetCount(layer).getOutput(0))
			if count2 > 0:
				print('%d objects of class %d selected' % (count2, fld_class))
				DM.Append(layer, outaa, "NO_TEST", "", "")
				DM.MakeFeatureLayer(outaa, outlyr)
				selectstr = '\"class\" = %d' % fld_class
				DM.SelectLayerByAttribute(outlyr, "NEW_SELECTION", "class = 0")
				DM.CalculateField(outlyr, "class", fld_class)
				DM.Delete(outlyr)
	DM.Delete(layer)
	DM.Delete(aalyr)
		
def add_shape_area(fc):
	fnames = []
	layer = "layer"
	fields = arcpy.ListFields(fc)
	DM.MakeFeatureLayer(fc, layer)
	for field in fields:
		fnames.append(field.name)
	if not ('Shape_Area' in fnames):
		print fc, ' has no shape area'
		DM.AddField(layer, "Shape_Area", "DOUBLE")
		DM.CalculateField(fc, "Shape_Area", "!shape.area@squaremeters!", "PYTHON_9.3", "#")
	DM.Delete(layer)	

def make_tile_index(workspace):
	fullnames = list_full_fcs(workspace)
	fcnames = list_filename_fcs(workspace)
	for i in range(0, len(fcnames)):
		outname = "%s/empty/%s" % (workspace, fcnames[i])
		DM.Dissolve(fullnames[i], outname)

def add_tile_label(workspace):
	fullnames = list_full_fcs(workspace)
	p1 = re.compile('tile(\d{1,3})\.shp')
	for fc in fullnames:
		print fc
		m1 = p1.search(fc)
		outstr = "\"%s\"" % m1.group(1)
		fields = arcpy.ListFields(fc)
		temp = []
		for field in fields:
			temp.append(field.name)
		if not ("Label" in temp):
			DM.AddField(fc, "Label", "TEXT", "", "", "3", "", "NON_NULLABLE", "NON_REQUIRED", "")	
		DM.CalculateField(fc, "Label", outstr)

	
def main():
#	rename_files(workspace)
#	fcnames = list_filename_fcs(workspace)
#	fullnames = list_full_fcs(workspace)
#	for fc in fullnames:
#		print fc
#		print "  killing zeroes...."
#		kill_zeroes(fc)
	fullnames = list_full_fcs(workspace)
	for fc in fullnames:
#		print fc
#		print "   getting samples from dissolve old samples MO"
#		add_class_within_dslv(fc, oldsamples_modslv, newsmpl_moexport)
#		print "   getting samples from dissolve old samples IL"
#		add_class_within_dslv(fc, oldsamples_ildslv, newsmpl_ilexport)
#		print "   getting samples from centroids old samples MO"
#		add_negclass_centroids(fc, oldsamples_mopts, newsmpl_moexport)
#		print "   getting samples from centroids old samples IL"
#		add_negclass_centroids(fc, oldsamples_ilpts, newsmpl_ilexport)
#		print "    getting aa sample objs"
#		get_aa_sampleobjs(fc, old_aa_pts, aa_objs)
		add_shape_area(fc)
#	make_tile_index(workspace)
#	emptyws = "%s/empty" % workspace
#	add_tile_label(emptyws)
#	add_shape_area(newsmpl_ilexport)
	
if __name__ == '__main__':	
	from arcpy import management as DM
	import arcpy
	import os
	import os.path
	import re
	
	workspace = 'u:\\EastWestGateway\\Objects\\Nuggets1_to_26_NDVI_redo\\Nugget40_IL'
	samplepath = 'u:/eastwestgateway/samples/'
	oldsamples_modslv = '%smo_samples_dslv.shp' % samplepath
	oldsamples_ildslv = '%sil_samples_dslv.shp' % samplepath
	oldsamples_mopts = '%smo_sample_centroids.shp' % samplepath
	oldsamples_ilpts = '%sil_sample_centroids.shp' % samplepath
	old_aa_pts = '%saa_sample_pts.shp' % samplepath

	newsmpl_moexport = '%smo_newsamples.shp' % samplepath
	newsmpl_ilexport = '%sil_newsamples.shp' % samplepath
	aa_fc = 'aa_newsamples.shp'
	aa_objs = '%s%s' % (samplepath, aa_fc)
	main()
