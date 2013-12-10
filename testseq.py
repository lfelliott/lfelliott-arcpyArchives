
#for i in range(20):#
#	iterator = 5 * (i + 1)
#	print iterator
#for i in range(5, 101, 5):
#		print i
num = 200
start =	5
gap = 5
landpos_divisor = int(num / gap)
for i in range(start, num + 1, gap):
	annulus_width = gap - 1
	j = i + annulus_width
	print str(i) + " to " + str(j)
print landpos_divisor
