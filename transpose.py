
def transpose_csv(inputfile, icolhdrfld, irownmfld, ivalfld):
# transpose_csv parameters:
#		inputfile - string, name of input csv file with headers
#		icolhdrfld - integer, number (starting from 0) of the field that will become column headers
#		irownmfld - integer, number (starting from 0) of the field that will become the row names
#		ivalfld - integer, number (starting from 0) of the field that will be used to populate the body of the table
# returns: list of strings (with carriage returns) of the transposed rows
#
# Input csv file:
# "LULC","SITE","COVER"
# "Grass", "Site 1", 20
# "Grass", "Site 2", 30
# "Woods", "Site 1", 10
#
# output = transpose_csv("input.csv", 0, 1, 2)
# Output:
#	"SITE","Grass","Woods"
#	"Site 1",20,10
#	"Site 2",30,0
#

# Get full list of unique covertypes and area names
	import csv
	columnheaders = []
	rownames = []
	newrows = []
	with open(inputfile) as csvfile:
		records = csv.reader(csvfile, delimiter = ',', quotechar='"')
		headers = records.next()
		for row in records:
			if (row[icolhdrfld] != headers[icolhdrfld]) & (not(row[icolhdrfld] in columnheaders)):
				columnheaders.append(row[icolhdrfld])
			if (row[irownmfld] != headers[irownmfld]) & (not(row[irownmfld] in rownames)):
				rownames.append(row[irownmfld])

# output header string			
	outstr = "\"" + headers[irownmfld] + "\""
	for column in columnheaders:
		outstr = outstr + ",\"" + column + "\""
	outstr = outstr + "\n"
	newrows.append(outstr)

	coverdict = {}
# Run through records for each area
	for name in rownames:	
		with open(inputfile) as csvfile:
# Set dictionary values to 0 for all covertypes
			for column in columnheaders:
				coverdict[column] = 0
			records = csv.reader(csvfile, delimiter = ',', quotechar='"')
			for row in records:
				if (row[irownmfld] == name):
					for column in columnheaders:
						if (row[icolhdrfld] == column):
							coverdict[column] = row[ivalfld]
		outstr = "\"" + name + "\""
		for column in columnheaders:
			outstr = outstr + "," + str(coverdict[column])
		outstr = outstr + "\n"
		newrows.append(outstr)
	return newrows

def main():
	for row in transpose_csv(infilename, 3, 5, 4):
		outfile.write(row)
	outfile.close()
	
if __name__ == '__main__':
	outfile = open('transposed.csv', 'w')
	infilename = 'CSV_Table_Wolf_Bayou_Other_12NOV14_1252.txt'		
	main()
	
