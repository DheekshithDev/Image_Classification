# CLIENT SIDE

import socket
import sys
import random
import threading
import os


class ClientSocket:

    def __init__(self, ip, port):
        self.image_data = None
        self.file = None
        self.sock = None
        self.TCP_SERVER_IP = ip
        self.TCP_SERVER_PORT = port
        self.connectCount = 0
        self.connect_server()

    def connect_server(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.TCP_SERVER_IP, self.TCP_SERVER_PORT))
            print(u'Client socket is connected with Server socket [ TCP_SERVER_IP: ' + self.TCP_SERVER_IP + ', TCP_SERVER_PORT: ' + str(self.TCP_SERVER_PORT) + ' ]')
            self.connectCount = 0
            self.send_images()
        except Exception as e:
            print(e)
            self.connectCount += 1
            if self.connectCount == 10:
                print(u'Connect fail %d times. exit program' % (self.connectCount))
                sys.exit()
            print(u'%d times try to connect with server' % (self.connectCount))
            self.connect_server()

    def send_images(self):
        try:
            path = r'C:\Users\Arthur King\OneDrive\Documents\My Docs\Class\COMPUTER NETWORKS 554 - 01 R Martin\Project\Images'
            r_file = random.choice(os.listdir(path))
            print('Image Chosen = ', r_file)
            self.file = open(os.path.join(path, r_file), 'rb')
            # self.file = open(r_file, 'rb')
            self.image_data = self.file.read(2048)

            while self.image_data:
                self.sock.send(self.image_data)
                self.image_data = self.file.read(2048)

            self.file.close()
            self.sock.close()

        except Exception as e:
            print(e)
            self.file.close()
            self.sock.close()


def main():
    IP = 'localhost'
    Port = 1004
    client = ClientSocket(IP, Port)


if __name__ == "__main__":
    main()