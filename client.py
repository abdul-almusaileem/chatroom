
#
#
import socket
import threading
import sys
import time


# define the Server's IP and connection port
#
HOST = "127.0.0.1"
PORT = 6676

# TODO: maybe find a way to send chuncks
#
BUFFER_SIZE = 1024

#
#
CLIENT_SOCK = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)


#
#
def main():
    try:
        CLIENT_SOCK.connect((HOST, PORT))
        receive_thread = threading.Thread(target=receive_msg)
        send_thread = threading.Thread(target=send_msg)
        receive_thread.start()
        send_thread.start()
    except socket.error as error:
        print "something happened: {}".format(error)


#
#
def receive_msg():
    try:
        while True:
            try:
                msg = CLIENT_SOCK.recv(BUFFER_SIZE).decode("utf-8")
                print "{}".format(msg)
                #time.sleep(2)
            except OSError:
                break
    except KeyboardInterrupt:
        sys.exit()
#
#
def send_msg():
    try:
        while True:
            time.sleep(1)
            msg = raw_input(">> ")
            try:
                CLIENT_SOCK.send(msg.encode("utf-8"))
                if msg == "{quit}":
                    CLIENT_SOCK.close()

            except KeyboardInterrupt:
                sys.exit()
    except KeyboardInterrupt:
        sys.exit()


# start main
#
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
