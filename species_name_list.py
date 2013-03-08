def uniq(input):
  output = []
  for x in input:
    if x not in output:
      output.append(x)

  return output
try:
	infile = open("texas_sp_names.txt", "r")
except IOError:
	print "The file does not exist"
outfile = open("namelist.txt", "w")
snames = []
snames2 = []
while 1:
	line = infile.readline()
	if not line: break
	fields = line.split(",")
	if (len(fields) == 3):
		sciname = fields[2]
		sciname = sciname[1:-2]
		names = sciname.split()
		for name in (names):
			snames.append(name)
snames2 = sorted(uniq(snames))
for sname in (snames2):
	outfile.write("%s\n" % sname)
	print(sname)
infile.close()
outfile.close()
	