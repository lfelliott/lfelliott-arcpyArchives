infile = open('images.txt', 'r')
georefd = []
while (1):
	line = infile.readline()[:-1]
	if not line: break
	georefd.append(line)
infile.close()
infile = open('hospimages.txt', 'r')
hosparpo = []
while (1):
	line = infile.readline()[:-1]
	if not line: break
	hosparpo.append(line)
infile.close()
outfile = open('missing_files2.txt', 'w')
for item in hosparpo:
	if item in georefd:
		print "%s is there" % item
	else:
		outfile.write("%s\n" % item)
