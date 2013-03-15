import re

infile = open("evt_legend.txt", 'r')
outfile = open("evt_legend.csv", 'a')
teststr = "123First value234Second value345ThirdValue"
line = infile.readline()
infile.close()
p1 = re.compile(r'\d+\D+')
p2 = re.compile(r'^(\d+)(.+)')
evtlist = p1.findall(line)
outfile.write("\"code\",\"name\"\n")
for item in evtlist:
#	print item
	m = p2.search(item)
	if m:
		code = m.group(1)
		name = m.group(2)
		outfile.write("%s,\"%s\"\n" % (code, name[1:]))
outfile.close()