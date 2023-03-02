# SERVER SIDE
import io
import socket
import threading
import cv2
import binascii
import base64
from PIL import Image
from numpy import array
from numpy import argmax
from keras.utils import to_categorical
import numpy
import tensorflow

# def recvall(sock, count):
#     buf = b''
#     while count:
#         newbuf = sock.recv(count)
#         if not newbuf: return None
#         buf += newbuf
#         count -= len(newbuf)
#     return buf

# FIXME: We tried ML pattern recognition and image classification on the string data of the image too.

# with open("t.png", "rb") as imageFile:
#     str = base64.b64encode(imageFile.read())
#     print str

class ServerSocket:

    def __init__(self, ip, port):
        self.image_chunk = None
        self.file = None
        self.addr = None
        self.conn = None
        self.sock = None
        self.TCP_IP = ip
        self.TCP_PORT = port
        self.socket_open()
        self.receiveThread = threading.Thread(target=self.receive_images)
        self.receiveThread.start()

        img_path = r"C:\Users\Arthur King\PycharmProjects\CN__Image_Project\server_image.jpg"

        # Byte Array Classification Process Part 1
        # image = Image.open(img_path)
        # hex_byte_array = binascii.hexlify(image.tobytes('raw'))
        # base_64_str = base64.b64encode(image.tobytes('raw'))
        # print('Org Byte Array = ', len(image.tobytes('raw')))
        # print('Hex Byte Array = ', len(hex_byte_array))
        # print('base_64_array = ', len(base_64_str))

        with open(img_path, 'rb') as image:
            f = image.read()
            # byte_array = bytearray(f)
            hex_byte_array = binascii.hexlify(f)
            base_64_str = base64.b64encode(f)
            print('Accurate Org Byte Array = ', len(f))
            print('Accurate Hex Byte Array = ', len(hex_byte_array))
            print('Accurate base_64_array = ', len(base_64_str))

            if len(f) < 100000 and len(hex_byte_array) < 250000:
                print('This is Real!')
            else:
                print('This is Animated!')

            data = [(1, 2), (0, 1), (2, 2), (2, 2)]
            data = array(data)
            print(data)
            # one hot encode
            encoded = to_categorical(data)
            print('encoded = ', encoded)
            # invert encoding
            inverted = argmax(encoded[0])
            print('inverted = ', inverted)

        # CV Part 1 - Bilateral Filtering Process CV
        # self.classify_1(img_path)

        # CV Part 2 - Color Count Process CV
        self.classify_2(img_path)

    def classify_2(self, path):
        img = cv2.imread(path)
        img = cv2.resize(img, (1024, 1024))
        a = {}
        for row in img:
            for item in row:
                value = tuple(item)
                if value not in a:
                    a[value] = 1
                else:
                    a[value] += 1

        mask = numpy.zeros(img.shape[:2], dtype=bool)
        for color, _ in sorted(a.items(), key=lambda pair: pair[1], reverse=True)[:512]:
            mask |= (img == color).all(-1)

        img[~mask] = (255, 255, 255)
        cv2.imshow("img", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        most_common_colors = sum([x[1] for x in sorted(a.items(), key=lambda pair: pair[1], reverse=True)[:512]])
        bool_checker = (most_common_colors / (1024 * 1024)) > 0.3
        print('bool_checker = ', bool_checker)
        if bool_checker:
            print("It's an Animated Image!")
        else:
            print("It's a Real Image!")

    def classify_1(self, path):
        img = cv2.imread(path)
        img = cv2.resize(img, (1024, 1024))
        color_blurred = cv2.bilateralFilter(img, 6, 250, 250)
        # Optional Preview
        cv2.imshow("blurred", color_blurred)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        diffs = []
        for k, color in enumerate(('b', 'r', 'g')):
            print(f"Comparing histogram for color {color}")
            real_histogram = cv2.calcHist(img, [k], None, [256], [0, 256])
            color_histogram = cv2.calcHist(color_blurred, [k], None, [256], [0, 256])
            diffs.append(cv2.compareHist(real_histogram, color_histogram, cv2.HISTCMP_CORREL))

        result = sum(diffs) / 3

        if result > 0.98:
            print("It's a cartoon!")
        else:
            print("It's a photo!")

    def socket_close(self):
        self.sock.close()
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is close')

    def socket_open(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.TCP_IP, self.TCP_PORT))
        self.sock.listen(1)
        self.sock.settimeout(1000)
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is open')
        self.conn, self.addr = self.sock.accept()
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is connected with client')

    def receive_images(self):
        try:
            self.file = open('server_image.jpg', 'wb')
            self.image_chunk = self.conn.recv(2048)

            while self.image_chunk:
                self.file.write(self.image_chunk)
                self.image_chunk = self.conn.recv(2048)

            self.file.close()
            self.socket_close()

        except Exception as e:
            print(e)
            self.file.close()
            self.socket_close()


def main():
    IP = 'localhost'
    Port = 1004
    server = ServerSocket(IP, Port)


if __name__ == "__main__":
    main()
