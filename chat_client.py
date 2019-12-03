"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def pad(string, size):
    string = str(string)
    if len(string) < size:
        return string+("-"*(size-len(string)))


def unpad(string):
    return string.replace("-", "")


def send(msg):
    try:
        # client_socket.send(bytes(msg, "utf8"))
        client_socket.send(bytes(str(pad(len(bytes(str(msg), "utf-8")), BUF) + msg), "utf-8"))

        if msg == "{quit}":
            client_socket.close()
            exit(0)
    except ConnectionResetError:
        print("Failed to connect to server, exiting")
        exit(0)


def receive():
    while True:
        try:
            # msg = client_socket.recv(BUFSIZ).decode("utf8")

            size = client_socket.recv(BUF)
            if not size:
                break
            msg = client_socket.recv(int(unpad(size.decode()))).decode()

            if msg:
                print(msg)
        except OSError:  # Possibly client has left the chat.
            break


def TKsend(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def TKreceive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    TKsend()


TK = False
if TK:
    import tkinter

    top = tkinter.Tk()
    top.title("Chat")

    messages_frame = tkinter.Frame(top)
    my_msg = tkinter.StringVar()  # For the messages to be sent.
    my_msg.set("Type your messages here.")
    scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
    # Following will contain the messages.
    msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    msg_list.pack()
    messages_frame.pack()

    entry_field = tkinter.Entry(top, textvariable=my_msg)
    entry_field.bind("<Return>", TKsend)
    entry_field.pack(fill=tkinter.X)
    send_button = tkinter.Button(top, text="Send", command=TKsend)
    send_button.pack()

    top.protocol("WM_DELETE_WINDOW", on_closing)


# ----Now comes the sockets part----
HOST = input('Enter host: ')
if not HOST:
    HOST = "10.237.19.122"
else:
    HOST = str(HOST)
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUF = 10
BUFSIZ = 1024
ADDR = (HOST, PORT)

try:
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDR)
except ConnectionRefusedError:
    print("Connection refused, server is probably down")
    exit(0)

if TK:
    receive_thread = Thread(target=TKreceive)
else:
    receive_thread = Thread(target=receive)
receive_thread.start()

if TK:
    tkinter.mainloop()  # Starts GUI execution.
else:
    while True:
        msg = input()
        send(msg)
