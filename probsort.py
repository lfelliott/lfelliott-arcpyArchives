# Takes a csv derived from randomForest predict(rf,x, type='prob) and determines the highest and second highest probabilities
# and reports the OBJECTID, best class, best class' probability, second best class, second best class' probability.
infile = open("probout2.csv", 'r')
outfile = open("probsort.csv", 'w')
labels = []
vals = []
probdict = {}
line = infile.readline()[:-1]
labels = line.split(',')
outstr = "\"OBJECTID\",\"BestClass\",\"BestProb\",\"SecondClass\",\"SecondProb\"\n"
outfile.write(outstr)
while (1):
	line = infile.readline()
	if not line: break
	vals = line.split(',')
	for i in (range(1,len(labels))):
		vals[i] = float(vals[i])
		probdict[labels[i]] = vals[i]
	sortedkeys = sorted(probdict, key=probdict.__getitem__, reverse=True)
	outstr = "%s,\"%s\",%0.3f,\"%s\",%0.3f\n" % (vals[0], sortedkeys[0], probdict[sortedkeys[0]], sortedkeys[1], probdict[sortedkeys[1]])
	outfile.write(outstr)
infile.close()
outfile.close()