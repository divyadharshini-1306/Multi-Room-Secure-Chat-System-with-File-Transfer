import socket
import ssl
import threading
from datetime import datetime
import os

HOST = "0.0.0.0"
PORT = 6000

rooms = {
    "AI": [],
    "CN": [],
    "ML": []
}

def broadcast(room, message, sender):
    for client in rooms[room]:
        if client != sender:
            try:
                client.send(message.encode())
            except:
                pass

def handle_client(conn, addr):

    print("Client connected:", addr)

    try:
        data = conn.recv(1024).decode()
        parts = data.split()

        if parts[0] == "JOIN":
            username = parts[1]
            room = parts[2]

        print(username + " joined room " + room)

        rooms[room].append(conn)

        while True:

            message = conn.recv(1024)

            if not message:
                break

            message = message.decode()

            if message.startswith("FILE"):
                parts = message.split()
                filename = parts[1]
                filesize = int(parts[2])

                with open("received_" + filename, "wb") as f:
                    remaining = filesize
                    while remaining > 0:
                        data = conn.recv(1024)
                        f.write(data)
                        remaining -= len(data)

                conn.send(f"File {filename} received".encode())
                continue

            timestamp = datetime.now().strftime("%H:%M:%S")
            full_message = f"[{timestamp}] {username}: {message}"

            print(full_message)

            broadcast(room, full_message, conn)

    except:
        pass

    conn.close()

def start_server():

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain("server.crt", "server.key")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((HOST, PORT))
    server.listen(5)

    print("Secure Chat Server Running on port", PORT)

    while True:

        client_socket, addr = server.accept()

        secure_socket = context.wrap_socket(client_socket, server_side=True)

        thread = threading.Thread(
            target=handle_client,
            args=(secure_socket, addr)
        )

        thread.start()

if __name__ == "__main__":
    start_server()
