"""This program module is the central server program. And is used to recieve data that are send from
the different GSM module inside the vehicle.And server module supposed to consist of GSM module and a
raspberry pi.The GSM module and raspberry pi is replaced with a single PC and internetwork""" 

import MySQLdb
import socket
import sys

db = MySQLdb.connect(host="localhost",user="root",passwd="root",db="speedb" )

cursor = db.cursor()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('192.160.1.3', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)
sock.listen(1)
print >>sys.stderr, 'waiting for a connection'

connection, client_address = sock.accept()
while True:
	try:
		
		vehicle_number = connection.recv(25)
		current_speed=connection.recv(25)
		print current_speed
		try:
			
			cursor.execute("SELECT * FROM  notification WHERE vehicle_number= %s",(vehicle_number))
			current_speed=int(current_speed)
			#print current_speed
			data=cursor.fetchall()
			if data==() and current_speed>45:
				cursor.execute("INSERT INTO notification(vehicle_number,msg_count,max_speed) VALUES ('%s','%d','%d' )" % (vehicle_number,3,current_speed))
			else:	
				cursor.execute("update notification set msg_count=%s WHERE vehicle_number= %s ",(data[0][1]+1,vehicle_number))
				if current_speed>int(data[0][2]):
					cursor.execute("update notification set max_speed=%s WHERE vehicle_number= %s ",(current_speed,vehicle_number))
			db.commit()
				
		except:
			# Rollback in case there is any error
			db.rollback()
	finally:
		print " "
connection.close()
