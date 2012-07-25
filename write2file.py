from datetime import date
print date.today()

strtoday = str(date.today())
outfile = open("c:/workspace/phase4/test8.txt", "a")
line = "This is a test1\n" + str(date.today())
outfile.writelines(line)
outfile.close()
line2 = "This is the 2nd line"
outfile = open("c:/workspace/phase4/test8.txt", "a")
outfile.writelines(line2)
outfile.close()