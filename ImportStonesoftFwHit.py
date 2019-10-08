#! /usr/bin/python

import sys
import os
import MySQLdb
import datetime
import time
from datetime import datetime, timedelta
import shutil

#Retrieve Arg (1 = filename, 2= tabName)
#MANUAL FILE CREATED BY COPY/PASTING the DATA OF THE FW COUNTER
filename = sys.argv[1]
#NAME OF THE FW
fwName = sys.argv[2]

#GetGlobalValue (id scan, date import...)
#date 
now = datetime.now()
date_import = now.strftime("%Y-%m-%d")

# Establish a MySQL connection
database = MySQLdb.connect (host="XXXXX", user = "XXXXX", passwd = "XXXXX", db = "XXXXX")

# Get the cursor, which is used to traverse the database, line by line
cursor = database.cursor()

#OUVERTURE FICHIER CSV FLUX ET IMPORT
try:
	f = open(filename, "r")
	next(f)
	for line in f:		
		c = line.split("\t")
		if c[13] != '':
			hit = c[13]
			rule_numberTmp = c[11].split('.')[0]
			rule_number = rule_numberTmp[1:]
			try :
				rule_number=int(rule_number)
				values = (hit, rule_number, fwName, 'stonesoft')
				query = """update firewall_flow_matrix set `obso_counter` = %s where rule_number = %s and firewall_name= %s and type_fw= %s"""
				cursor.execute(query,values)
			except Exception as e:
				continue
	f.close()
	# Close the cursor
	cursor.close()
	# Commit the transaction
	database.commit()
	print("Insertion of Stonesoft Flow Matrix OK")
except Exception as e:
	print ("Insertion of Stonesoft Flow Matrix failed "+str(e))
	cursor.close()
	sys.exit(1)

# Close the database connection
database.close()




# Print results
print ""
print "All Done!"
print ""
