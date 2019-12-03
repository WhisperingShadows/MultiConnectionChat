"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time


def pad(string, size):
    string = str(string)
    if len(string) < size:
        return string + ("-" * (size - len(string)))


def unpad(string):
    return string.replace("-", "")


def send(msg, client):
    try:
        # client_socket.send(bytes(msg, "utf8"))
        client.send(bytes(str(pad(len(bytes(str(msg), "utf-8")), BUF) + msg), "utf-8"))

        if msg == "{quit}":
            client.close()
            exit(0)
    except ConnectionResetError:
        print("Failed to connect to client")


def receive(client):
    while True:
        try:
            # msg = client_socket.recv(BUFSIZ).decode("utf8")

            size = client.recv(BUF)
            if not size:
                break
            msg = client.recv(int(unpad(size.decode()))).decode()
            if msg:
                try:
                    print("%s: " % clients[client] + msg)
                except KeyError:
                    pass
                return(msg)
        except OSError:  # Possibly client has left the chat.
            break





def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s has connected." % str(client_address))
        # client.send(bytes("Hello there! Please enter your name and press enter!", "utf8"))
        send("Hello there! Please enter your name and press enter!", client)
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,), daemon=True).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    # name = client.recv(BUFSIZ).decode("utf8")
    name = receive(client)
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    # client.send(bytes(welcome, "utf8"))
    send(welcome, client)
    msg = "%s has joined the chat!" % name
    # broadcast(bytes(msg, "utf8"), client)
    broadcast(msg, client)
    clients[client] = name

    while True:
        try:
            # msg = client.recv(BUFSIZ)
            msg = receive(client)

            if msg == "{quit}":
                # client.send(bytes("{quit}", "utf8"))
                client.close()
                del clients[client]
                # broadcast(bytes("%s has left the chat." % name, "utf8"), client)
                broadcast("%s has left the chat." % name, client)
                print("%s has disconnected." % str(addresses[client]))
                break
            else:
                broadcast(msg, client, name + ": ")
        except ConnectionResetError:
            client.close()
            del clients[client]
            # broadcast(bytes("%s has left the chat." % name, "utf8"), client)
            broadcast("%s has left the chat." % name, client)
            print("%s has disconnected." % str(addresses[client]))
        except OSError:
            return

def byt(string):
    return bytes(string, "utf-8")


def broadcast(msg, client, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        if sock != client:
            # sock.send(bytes(prefix, "utf8") + msg)
            if msg:
                send(prefix+msg, sock)


clients = {}
addresses = {}

HOST = '10.237.19.122'
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
BUF = 10

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections, daemon=True)
    ACCEPT_THREAD.start()

    while True:
        ms = input()
        if ms == "conns":
            print(len(clients))
        elif ms == "exit":
            # broadcast(byt("Internal server initiating shutdown"), SERVER, "Server: ")
            broadcast("Initiating internal server shutdown", SERVER, "Server: ")
            time.sleep(3)
            exit(0)

            exit(0)
        elif ms[:5] == "/say ":
            # broadcast(byt(ms[5:]), SERVER, "Server: ")
            broadcast(ms[5:], SERVER, "Server: ")
        else:
            print("Invalid command")

    #ACCEPT_THREAD.join()
    #SERVER.close()
