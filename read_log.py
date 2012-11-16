import time, os

#Set the filename and open the file
os.chdir("c:\Cumulus\data")
filename = 'Nov12log.txt'
file = open(filename,'r')

#Find the size of the file and move to the end
st_results = os.stat(filename)
st_size = st_results[6]
file.seek(st_size)

while 1:
    where = file.tell()
    line = file.readline()
    if not line:
        time.sleep(1)
        file.seek(where)
    else:
		(date, time, temp, humidity, dewpt, windspd, gust, windbrng, rainrate, raintoday, pressure, raintotal, insidetemp, insidehum, currentgust, windchill, htndx, uvndx, solar, evapo, annualevapo, apparenttemp, maxsolar, hrssunshine, currentwindbearing) = line.split(r',')
#        print line, # already has newline
		print insidetemp