import socket
import ssl
import threading
import os
import re

PORT = 6000


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


def send_file(sock, filename):
    if not os.path.exists(filename):
        print("File not found")
        return

    filesize = os.path.getsize(filename)

    sock.send(f"FILE {filename} {filesize}".encode())

    with open(filename, "rb") as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            sock.send(data)

    print("File sent")


def start_client():

    server_ip = input("Enter server IP address: ")

    context = ssl._create_unverified_context()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    secure_socket = context.wrap_socket(sock, server_hostname=server_ip)

    secure_socket.connect((server_ip, PORT))

    # 🔥 Receive room list from server
    print(secure_socket.recv(1024).decode())

    # Username
    while True:
        username = input("Enter username: ")
        if valid_username(username):
            break
        else:
            print("Invalid username")

    # Choose room
    room = input("Choose room: ")

    secure_socket.send(f"JOIN {username} {room}".encode())

    thread = threading.Thread(
        target=receive_messages,
        args=(secure_socket,)
    )
    thread.start()

    print("\nCommands:")
    print("/msg username → start private chat")
    print("/leave_private → exit private chat\n")

    try:
        while True:

            message = input()

            if message.startswith("/sendfile"):
                parts = message.split()
                if len(parts) == 2:
                    send_file(secure_socket, parts[1])
                else:
                    print("Usage: /sendfile filename")
            else:
                secure_socket.send(message.encode())

    except KeyboardInterrupt:
        print("\nExiting...")
        secure_socket.close()


if __name__ == "__main__":
    start_client()
