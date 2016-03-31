import csv
mydict = {1: "test1", 3: "test3", 4: "test4"}
writer = csv.writer(open('dict.csv', 'wb'))
for key, value in mydict.items():
	writer.writerow([key, value])