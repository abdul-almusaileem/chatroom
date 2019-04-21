
# this is a server for a multi connection clients
# when it reacieves a data it passes the data to all other clients
#

import socket
import threading
import  sys
import pickle
from time import time

# define the Server's IP and connection port
#
HOST = "127.0.0.1"
PORT = 6676

# TODO: maybe find a way to send chuncks
#
BUFFER_SIZE = 1024

#
#
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



# keep track of users connected and the addresses
# {sock: }
#
clients = {}
addresses = {}

# start the server and the threading process
#
def main():

    #
    #
    try:
        SERVER.bind((HOST, 6676))
        SERVER.listen(2)
        print "waiting for connections..."

        try:
            server_thread = threading.Thread(target=accept_clients, args=(SERVER, ))
            server_thread.start()
            server_thread.join()
        except (KeyboardInterrupt, SystemExit):
            #cleanup_stop_thread()
            sys.exit()
    #
    #
    except socket.error as err:
        pass
        print err

    #
    #
    finally:
        SERVER.close()

# a method to estaplish connection with new clients each on a different thread
# as it waits forever for connections to come
#
def accept_clients(server):
    while True:
        # get the new connection
        #
        client, client_address = server.accept()

        print "{} just joined the room".format(client_address)

        client.send("Hello, what is your name ?".encode("utf-8"))
        addresses[client] = client_address

        try:
            threading.Thread(target=chatroom, args=(client, )).start()
        except (KeyboardInterrupt, SystemExit):
            #cleanup_stop_thread()
            sys.exit()


# Chatroom meathod to
#
def chatroom(client):

    # get the client's name
    # and add it to the clients list
    #
    name = client.recv(BUFFER_SIZE).decode("utf8")
    clients[client] = name

    # send a welcome meassage
    # and send a Broadcast meassage to notify everyone
    #
    client.send("Hello {}, welcome to the Chatroom...!".format(clients[client]).encode("utf-8"))

    msg = "\n{}, has just Joined the Chatroom...".format(clients[client])
    broadcast_msg(msg.encode("utf-8"))

    # start the Chatroom
    #
    #
    while True:
        # get the meassage from the user
        #
        msg = client.recv(BUFFER_SIZE)

        # check if quit was recieves: then send a a Goodbye meassage
        # if starts with @[name]: send the meassage only to that person
        # else: send the meassage to everyone.
        #
        if msg == "quit".encode("utf-8"):
            client.send("Goodbye".encode("utf-8"))
            client.send("quit".encode("utf-8"))
            client.close()
            del clients[client]
            broadcast_msg("{} left the Chatroom\n".format(clients[client]).encode("utf-8"))
            break

        elif msg.startswith("@"):
            no_at_msg = msg.strip("@")

            spaced = no_at_msg.split(" ")

            msg_to = spaced[0]
            del spaced[0]

            msg = " ".join(spaced)

            # get the client from the name
            #
            for client_sock, client_name in clients.iteritems():
                if client_name == msg_to:
                    send_msg_to(clients[client], msg, client_sock)

        else:
            broadcast_msg(msg, clients[client])

# send the recieved meassage to connected cliens
#
def broadcast_msg(msg, name=""):
    for sock in clients:
        sock.send("{}: {}\n".format(name, msg).encode("utf-8"))

# given a msg send it to the specified client
#
def send_msg_to(msg_by, msg, client_sock):
    pass
    client_sock.send("Private meassage from {}: {}".format(msg_by, msg).encode("utf-8"))




if __name__ == '__main__':
    main()
