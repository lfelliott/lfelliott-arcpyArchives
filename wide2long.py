infile = open("sgp_ta.csv", 'r')
outfile = open("sgp_ta_long.csv", 'a')
i = 0

while (1):
	i = i + 1
	fields = []
	outstr = ''
	line = infile.readline()[0:-1]
	if not line: break
	fields = line.split(',')
	if i == 1: 
		headers = fields
	else:
		for j in range(1, len(fields)):
			outstr = "%s,%s,%s\n" % (fields[0],headers[j],fields[j])
			outfile.write(outstr)
infile.close()
outfile.close()

	