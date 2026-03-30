import socket
import ssl
import threading
import time
from datetime import datetime

HOST = "0.0.0.0"
PORT = 6000

rooms = {"AI": [], "CN": [], "ML": []}
users = {}
lock = threading.Lock()

total_bytes = 0
start_time = time.time()


def get_room_info():
    info = "Rooms:\n"
    for room in rooms:
        info += f"{room}: {len(rooms[room])} users\n"
    return info


def get_users():
    info = "\nActive Users:\n"
    for r in rooms:
        names = [u for _, u in rooms[r]]
        info += f"{r}: {', '.join(names) if names else 'None'}\n"
    return info


def broadcast(room, message):
    global total_bytes
    if room not in rooms:
        return

    data = (message + "\n").encode()

    for client, user in rooms[room][:]:
        try:
            client.send(data)
            total_bytes += len(data)
        except:
            rooms[room].remove((client, user))


def monitor_performance():
    global total_bytes, start_time
    while True:
        time.sleep(5)
        elapsed = time.time() - start_time

        if elapsed > 0:
            throughput = total_bytes / elapsed / 1024
            if throughput > 0.1:
                print(f"[PERFORMANCE] Throughput: {throughput:.2f} KB/s")

        total_bytes = 0
        start_time = time.time()


def handle_client(conn, addr):
    global total_bytes

    print(f"[NEW CONNECTION] {addr}")
    username = None
    room = None

    try:
        conn.send((get_room_info() + "\n").encode())

        data = conn.recv(1024).decode().strip()
        parts = data.split()

        if len(parts) < 3 or parts[0] != "JOIN":
            return

        username, room = parts[1], parts[2]

        with lock:
            rooms[room].append((conn, username))
            users[username] = {"conn": conn, "room": room}

        print(f"[JOIN] {username} joined {room}")
        conn.send((get_users() + "\n").encode())

        while True:
            data = conn.recv(1024)
            if not data:
                break

            message = data.decode().strip()
            total_bytes += len(data)

            # PING
            if message == "PING":
                conn.send("PONG\n".encode())
                continue

            # USERS
            if message.startswith("/users"):
                conn.send((get_users() + "\n").encode())
                continue

            # PRIVATE
            if message.startswith("/msg"):
                parts = message.split(" ", 2)
                if len(parts) < 3:
                    continue

                target = parts[1]
                content = parts[2]

                if "||" in content:
                    msg, ts = content.rsplit("||", 1)
                    rt = round((time.time() - float(ts)) * 1000, 2)
                else:
                    msg, rt = content, 0

                timestamp = datetime.now().strftime("%H:%M:%S")

                if target in users:
                    users[target]["conn"].send(
                        f"[{timestamp}] {username} (private): {msg} (RTT: {rt} ms)\n".encode()
                    )
                    conn.send(f"[SENT to {target}]\n".encode())

                continue

            # FILE TRANSFER
            if message.startswith("FILE"):
                parts = message.split()
                target, filename, size = parts[1], parts[2], int(parts[3])

                file_data = b""
                while len(file_data) < size:
                    chunk = conn.recv(4096)
                    file_data += chunk
                    total_bytes += len(chunk)

                if target in users:
                    target_conn = users[target]["conn"]
                    target_conn.send(f"FILE {username} {filename} {size}\n".encode())
                    target_conn.sendall(file_data)

                continue

            # EXIT
            if message == "/exit":
                break

            # NORMAL MESSAGE
            if "||" in message:
                msg, ts = message.rsplit("||", 1)
                rt = round((time.time() - float(ts)) * 1000, 2)
            else:
                msg, rt = message, 0

            timestamp = datetime.now().strftime("%H:%M:%S")
            full_msg = f"[{timestamp}] {username}: {msg} (RTT: {rt} ms)"

            print(full_msg)
            broadcast(room, full_msg)

    except Exception as e:
        print("[ERROR]", e)

    finally:
        with lock:
            if username in users:
                del users[username]
            if room in rooms:
                rooms[room] = [(c, u) for c, u in rooms[room] if c != conn]

        if username:
            broadcast(room, f"{username} left the chat")

        conn.close()


def start_server():
    print("Starting Secure Chat Server...")

    threading.Thread(target=monitor_performance, daemon=True).start()

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain("server.crt", "server.key")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"[SUCCESS] Server running on {HOST}:{PORT}")
    print("Waiting for clients...\n")

    while True:
        client_socket, addr = server.accept()
        secure_socket = context.wrap_socket(client_socket, server_side=True)

        threading.Thread(target=handle_client, args=(secure_socket, addr), daemon=True).start()


if __name__ == "__main__":
    start_server()
