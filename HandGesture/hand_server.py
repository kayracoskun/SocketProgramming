"""
server.py

if you get an error with s.bind((self.host, self.address))
check the port and find an unused port
"""
import socket
import random
import time


class Connect():
    def __init__(self):
        # Create a socket (connecting two computers)
        try:
            self.host = ""
            self.port = 9999
            self.s = socket.socket()
            self.bind_socket()
        except socket.error as msg:
            print(f"Socket couldn't be created. Error {msg}")

    def bind_socket(self):
        # Binding the socket and listening for connections
        try:
            print(f"Binding the port {str(self.port)}")

            self.s.bind((self.host, self.port))
            self.s.listen(2)  # we are listenning for 2 connection
            self.socket_accept()

        except socket.error as msg:
            print(f"Socket binding error {str(msg)} Retrying...")
            self.bind_socket()  # by using recursion we are trying to connect

    def socket_accept(self):
        # Establish connection with a client (socket must be listenning)
        # conn will be the object of a connection, address is the list of ip and port
        self.conn, address = self.s.accept()
        print(
            f"Connection has been established. | IP: {address[0]} Port: {str(address[1])}")

    def send_command(self, data):
        # Send commands to client
        try:
            self.conn.send(str.encode(data))
            # to recieve information from client
            client_response = str(self.conn.recv(1024), "utf-8")
            print(client_response)
        except:
            self.conn.close()
            print("Connection closed.")


if __name__ == "__main__":
    connect = Connect()
    while True:
        try:
            data = str(random.randint(1, 5))
            connect.send_command(data)
            time.sleep(2)
        except:
            print("Connection lost.")
            break
