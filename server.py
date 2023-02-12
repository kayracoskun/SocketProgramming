"""
server.py

if you get an error with s.bind((self.host, self.address))
check the port and find an unused port
"""
import socket


class Connect():
    def __init__(self):
        # Create a socket (connecting two computers)
        try:
            self.host = ""
            self.port = 9998
            self.s = socket.socket()
            self.bind_socket()
        except socket.error as msg:
            print(f"Socket couldn't be created. Error {msg}")

    def bind_socket(self):
        # Binding the socket and listening for connections
        try:
            print("Binding the port " + str(self.port))

            self.s.bind((self.host, self.port))
            self.s.listen(1)  # we are listenning for 1 connection
            self.socket_accept()

        except socket.error as msg:
            print("Socket binding error " + str(msg) + "Retrying...")
            self.bind_socket()  # by using recursion we are trying to connect

    def socket_accept(self):
        # Establish connection with a client (socket must be listenning)
        # conn will be the object of a connection, address is the list of ip and port
        conn, address = self.s.accept()
        print("Connection has been established. IP: " +
              address[0] + " Port: "+str(address[1]))

        # whenever we want to send something we will use this conn object
        self.send_command(conn)

        conn.close()

    def send_command(self, conn):
        # Send commands to client
        while True:
            user_input = input("Enter something: ")

            if len(str.encode(user_input)) > 0:
                conn.send(str.encode(user_input))
                # to recieve information from client
                client_response = str(conn.recv(1024), "utf-8")
                print(client_response)


if __name__ == "__main__":
    connect = Connect()
