#!/usr/bin/python

import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","cloud","cloud","userdb" )

# prepare a cursor object using cursor() method
cursor = db.cursor()
username="don"
pas="mushkil hai "


sql="INSERT INTO user(username,password) VALUES ('%s','%s' )" % (username,pas)
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Commit your changes in the database
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()

# disconnect from server
db.close()
