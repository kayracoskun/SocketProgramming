"""
client.py
	- try and connect to our server
	- wait for our instructions
	- receives the instructions and run them
	- take the results and send them back to the server
"""
import socket

s = socket.socket()
host = "192.168.1.38"
port = 9999

s.connect((host, port))

while True:
    try:
        data = s.recv(1024)
        print(data.decode("utf-8"))

        s.send(str.encode("Done"))

    except socket.error as msg:
        print(f"Connection lost. {msg}")
        break
