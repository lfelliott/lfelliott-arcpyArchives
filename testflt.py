line = "[38, 30, 2020/1010]"
import re
def convertll(ll):
	m = re.search(r'(\d+), (\d+), (\d+)\/(\d+)', ll)
	deg = float(m.group(1))
	min = float(m.group(2))
	sec = float(m.group(3))
	secfrac = float (m.group(4))
	decll = deg + (min/60) + ((sec/secfrac)/3600)
	return float(decll)
print "%.7f" % convertll(line)
