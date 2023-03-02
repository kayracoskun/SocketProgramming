import socket
import cv2
import pickle
import struct


class Connect():
    def __init__(self):
        try:
            self.host = ""
            self.port = 9999
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Socket created")
            self.bind_socket()
        except socket.error as msg:
            print(f"Socket couldn't be created. {msg}")

    def bind_socket(self):
        try:
            print("Binding the port " + str(self.port))
            print("Waiting for connection")

            self.s.bind((self.host, self.port))
            self.s.listen(5)
            self.socket_accept()

        except socket.error as msg:
            print("Socket binding error " + str(msg) + "Retrying...")
            self.bind_socket()

    def socket_accept(self):
        conn, address = self.s.accept()
        print("Connection established at IP: " +
              address[0] + " & Port: "+str(address[1]))

        self.send_command(conn)

        conn.close()

    def send_command(self, conn):
        while True:
            try:
                vid = cv2.VideoCapture(0)
                while(vid.isOpened()):
                    img, frame = vid.read()
                    a = pickle.dumps(frame)
                    message = struct.pack("Q", len(a))+a
                    conn.sendall(message)
                    cv2.imshow('Sending...', frame)
                    if cv2.waitKey(20) & 0xFF == ord('q'):
                        break

            except:
                conn.close()
                print("\nConnection closed.")
                break


if __name__ == "__main__":
    connect = Connect()
