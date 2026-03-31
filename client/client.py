import socket
import ssl
import threading
import time
import os
import re

PORT = 6000
latency_flag = False


def valid_username(name):
    return re.match(r'^[A-Za-z0-9_]+$', name)


def receive(sock):  
    global latency_flag
    buffer = b""

    while True:
        try:
            data = sock.recv(4096)
            if not data:
                break

            buffer += data

            while b"\n" in buffer:
                line, buffer = buffer.split(b"\n", 1)
                msg = line.decode()

                if msg == "PONG":
                    latency_flag = True
                    continue

                if msg.startswith("FILE"):
                    parts = msg.split()
                    sender, filename, size = parts[1], parts[2], int(parts[3])

                    print(f"\nReceiving '{filename}' from {sender}...")

                    file_data = b""
                    while len(file_data) < size:
                        file_data += sock.recv(4096)

                    with open("received_" + filename, "wb") as f:
                        f.write(file_data)

                    print(f"Saved as received_{filename}")
                    continue

                print(msg)

        except:
            print("Disconnected from server")
            break


def ping(sock):
    global latency_flag
    latency_flag = False

    start = time.time()
    sock.send("PING\n".encode())

    timeout = 2
    while not latency_flag and timeout > 0:
        time.sleep(0.01)
        timeout -= 0.01

    if latency_flag:
        latency = round((time.time() - start) * 1000, 2)
        print(f"Latency: {latency} ms")
    else:
        print("Ping failed")


def send_file(sock, target, filename):
    if not os.path.exists(filename):
        print("File not found. Create it first.")
        return

    size = os.path.getsize(filename)

    sock.send(f"FILE {target} {filename} {size}\n".encode())

    with open(filename, "rb") as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            sock.sendall(chunk)

    print(f"File '{filename}' sent to {target}")


def start():
    ip = input("Enter server IP: ")

    context = ssl._create_unverified_context()
    sock = socket.socket()
    sock = context.wrap_socket(sock, server_hostname=ip)

    sock.connect((ip, PORT))    
    print(sock.recv(1024).decode())

    while True:
        username = input("Enter username: ")
        if valid_username(username):
            break
        print("Invalid username")

    room = input("Choose room (AI/CN/ML): ")
    sock.send(f"JOIN {username} {room}\n".encode())
    print(sock.recv(1024).decode())

    threading.Thread(target=receive, args=(sock,), daemon=True).start()

    print("\n===== COMMANDS =====")
    print("/msg <user> <message>")
    print("/users")
    print("/sendfile <user> <file>")
    print("/ping")
    print("/exit")
    print("====================\n")

    while True:
        msg = input()

        if msg == "/ping":
            ping(sock)

        elif msg == "/users":
            sock.send("/users\n".encode())

        elif msg.startswith("/sendfile"):
            parts = msg.split()
            if len(parts) < 3:
                print("Usage: /sendfile user filename")
                continue
            send_file(sock, parts[1], parts[2])

        elif msg.startswith("/msg"):
            parts = msg.split(" ", 2)
            if len(parts) < 3:
                print("Usage: /msg user message")
                continue
            ts = time.time()
            sock.send(f"/msg {parts[1]} {parts[2]}||{ts}\n".encode())
        
        elif msg == "/exit":
            sock.send("/exit\n".encode())
            print("Disconnecting...")
            sock.close()
            break

        else:
            ts = time.time()
            sock.send(f"{msg}||{ts}\n".encode())


if __name__ == "__main__":
    start()
