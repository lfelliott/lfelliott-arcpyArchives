import arcpy
# Add layer labels from attributes. In this case, each value must have a unique label within a field of the attribute table.
# You need to have a project with the layer as type Unique Values (Categories|Unique Values)
# Close the project, run the script and reopen the project. Hopefully the layer labels will be filled out.
# Test case that I ran it on:
#  Map document: test.mxd
#  Layer: patch_area2
#  Value Field: Id
#  Label Field: idname

mapname = "test.mxd"
layername = "patch_area2"
valfld = "Id"
labfld = "idname"

mxd = arcpy.mapping.MapDocument(mapname) 
lyr = arcpy.mapping.ListLayers(mxd, layername)[0]

# Make sure the symbology type is unique values and add all the values
print "Working on: " + layername

if lyr.symbologyType == "UNIQUE_VALUES":
	lyr.symbology.valueField = valfld
	lyr.symbology.addAllValues()
else:
	print "Error: Layer must be of type Unique Values"
	exit()
	
labellist = []

# Get all the labels in ascending order
sqlstr = "ORDER BY %s ASC" % valfld
rows = arcpy.da.SearchCursor(lyr, "idname", sql_clause=(None, sqlstr))
for row in rows:
	labellist.append(row[0])

# Make the labels unique	
uniquevalues = set(labellist)
labellist = []
for item in uniquevalues:
	labellist.append(item)

lyr.symbology.classLabels = labellist


arcpy.RefreshActiveView()
arcpy.RefreshTOC()
mxd.save()
del mxd
