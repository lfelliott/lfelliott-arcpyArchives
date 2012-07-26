import pyodbc
dbname = 'c:\\workspace\\Phase5\\Objects\\Phase5Key.mdb'
sqlstr = 'SELECT * FROM Phase5Key;'
#sources = pyodbc.dataSources()
#for source in sources:
#	print source
con = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)}; DBQ=c:\\workspace\\Phase5\\Objects\\Phase5Key.mdb;')
cur = con.cursor()
cur.execute(sqlstr)
rows = cur.fetchall()
for row in rows:
	ecogrp = row.EcoGroup
	if row.gt_elev is None:
		print ecogrp
