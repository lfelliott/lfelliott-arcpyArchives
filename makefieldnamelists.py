import arcpy
from arcpy import management as DM

outfile = open("mdc_elt_fields.txt", "a")
arcpy.env.workspace = "F:/Projects/EnduringFeatures/mo_elt/MDC_ESC.gdb"
fcs = arcpy.ListFeatureClasses("*")
for fc in (fcs):
	desc = arcpy.Describe(fc)
	fields = desc.fields
	for field in fields:
		outstr = "\"%s\", \"%s\"\n" % (fc, field.name)
		outfile.write(outstr)
