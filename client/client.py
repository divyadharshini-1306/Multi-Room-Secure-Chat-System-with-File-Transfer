import socket
import ssl
import threading
import time
import os
import re

PORT = 6000
latency_flag = False


# 🔹 USERNAME VALIDATION
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
                    sender = parts[1]
                    filename = parts[2]
                    size = int(parts[3])

                    file_data = b""
                    while len(file_data) < size:
                        chunk = sock.recv(4096)
                        file_data += chunk

                    with open("received_" + filename, "wb") as f:
                        f.write(file_data)

                    print(f"\nFile received from {sender}")
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
    time.sleep(0.5)

    if latency_flag:
        latency = (time.time() - start) * 1000
        print(f"Latency: {int(latency)} ms")
    else:
        print("Ping failed")


def send_file(sock, target, filename):
    if not os.path.exists(filename):
        print("File not found")
        return

    size = os.path.getsize(filename)

    sock.send(f"FILE {target} {filename} {size}\n".encode())

    with open(filename, "rb") as f:
        sock.sendall(f.read())

    print("File sent")


def start():
    ip = input("Enter server IP: ")

    context = ssl._create_unverified_context()
    sock = socket.socket()
    sock = context.wrap_socket(sock, server_hostname=ip)

    sock.connect((ip, PORT))

    print(sock.recv(1024).decode())

    # 🔹 VALIDATED USERNAME LOOP
    while True:
        username = input("Enter username: ")
        if valid_username(username):
            break
        else:
            print("Invalid username! Use only letters, numbers, underscore.")

    room = input("Choose room (AI/CN/ML): ")

    sock.send(f"JOIN {username} {room}\n".encode())

    print(sock.recv(1024).decode())

    threading.Thread(target=receive, args=(sock,), daemon=True).start()

    print("\n===== COMMANDS =====")
    print("Type message → broadcast")
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

        elif msg.startswith("/sendfile"):
            parts = msg.split()
            if len(parts) < 3:
                print("Usage: /sendfile user filename")
                continue
            send_file(sock, parts[1], parts[2])

        else:
            sock.send((msg + "\n").encode())


if __name__ == "__main__":
    start()
