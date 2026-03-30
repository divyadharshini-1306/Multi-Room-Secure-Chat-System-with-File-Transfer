import socket
import ssl
import threading
import os
import re

PORT = 6000

rooms = ["AI", "CN", "ML"]

def receive_messages(sock):

    while True:
        try:
            message = sock.recv(1024).decode()
            if message:
                print(message)
        except:
            break


def valid_username(name):

    pattern = r'^[A-Za-z0-9_]+$'
    return re.match(pattern, name)
    # Room selection


            break

    join_message = f"JOIN {username} {room}"

    thread = threading.Thread(
        target=receive_messages,
        args=(secure_socket,)
    )
    thread.start()

    print("\nCommands:")
    print("/users → show users in room")
    print("/sendfile filename → send file\n")

    try:
        while True:

            message = input()

            if message.startswith("/sendfile"):
if __name__ == "__main__":
    start_client()

                parts = message.split()


                if len(parts) == 2:
        secure_socket.close()
                    send_file(secure_socket, parts[1])
        print("\nClient exiting...")

    except KeyboardInterrupt:
                else:
                    print("Usage: /sendfile filename")

            else:
                secure_socket.send(message.encode())

    secure_socket.send(join_message.encode())
            print("Invalid room. Choose from:", rooms)
        else:
        if room in rooms:
        room = input("Choose a room: ")

    while True:
    print("Available rooms:", rooms)
            break
            print("Invalid username. No special characters allowed.")

        else:

        username = input("Enter username (letters, numbers, _ only): ")

        if valid_username(username):


def send_file(sock, filename):

    # Username validation
    while True:

    if not os.path.exists(filename):
    secure_socket.connect((server_ip, PORT))

        print("File not found")
        return

    secure_socket = context.wrap_socket(sock, server_hostname=server_ip)
    filesize = os.path.getsize(filename)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    sock.send(f"FILE {filename} {filesize}".encode())

    with open(filename, "rb") as f:
    context = ssl._create_unverified_context()
        while True:
            data = f.read(1024)

    server_ip = input("Enter server IP address: ")


def start_client():
            if not data:

