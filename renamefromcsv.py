import csv
import os
rows = csv.reader(open('filelist.csv', 'rb'), delimiter = ',', quotechar='"')
for row in rows:
	var1 = row[0]
	var2 = var1[0] + row[1].strip() + '.csv'
	print var1
	print var2
	if os.path.exists(var1):
		os.rename(var1, var2)
	

	