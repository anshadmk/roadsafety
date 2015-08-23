"""
This module is used to simlate the the speed sensoring,
transmission of speed measurment via GSM module.
This module generate speed measurement values which is 
used to compare with the maximum speed""" 


import socket
import sys
import socket
import random
import time
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening
server_address = ('192.160.1.3', 10000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)
while True:
	time.sleep(2)
	random_speed= str(random.randint(1, 100))
	print "speed  : ",random_speed
	if random_speed>45:
		sock.sendall("KL 7 AJ 1080")
		sock.sendall(random_speed)
sock.close()
    
