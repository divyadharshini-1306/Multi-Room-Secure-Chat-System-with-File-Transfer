import socket
import ssl
import threading
import time
import re
from datetime import datetime

HOST = "0.0.0.0"
PORT = 6000

rooms = {"AI": [], "CN": [], "ML": []}
users = {}
lock = threading.Lock()

total_bytes = 0
start_time = time.time()

MAX_MSG_SIZE = 8192


def valid_username(name):
    return re.match(r'^[A-Za-z0-9_]+$', name)


def get_room_info():
    info = "Available Rooms:\n"
    for room in rooms:
        info += f"{room}\n"
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

    with lock:
        clients = list(rooms[room])

    for client, user in clients:
        try:
            client.sendall(data)
            total_bytes += len(data)
        except:
            with lock:
                rooms[room] = [(c, u) for c, u in rooms[room] if c != client]


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


def recv_exact(conn, size):
    data = b""
    while len(data) < size:
        chunk = conn.recv(min(4096, size - len(data)))
        if not chunk:
            raise ConnectionError("Connection lost during file transfer")
        data += chunk
    return data


def handle_client(conn, addr):
    global total_bytes

    print(f"[NEW CONNECTION] {addr}")
    username = None
    room = None
    buffer = b""

    try:
        conn.send((get_room_info() + "\n").encode())

        # ✅ JOIN LOOP (RETRY UNTIL VALID)
        while True:
            while b"\n" not in buffer:
                data = conn.recv(4096)
                if not data:
                    conn.close()
                    return
                buffer += data

            line, buffer = buffer.split(b"\n", 1)
            
            message = line.decode(errors="ignore").strip()

            # ✅ Remove timestamp if present
            if "||" in message:
                message = message.split("||")[0]

		#print(message)
            parts = message.split()
            print(parts)

            if len(parts) < 3 or parts[0] != "JOIN":
                conn.send("Invalid JOIN format. Use: JOIN <username> <room>\n".encode())
                continue

            username, room = parts[1], parts[2]
            print(room)

            if not valid_username(username):
                conn.send("❌ Invalid username format\n".encode())
                continue

            if room not in rooms:
                conn.send(
                    "❌ No such room.\nChoose from: AI, CN, ML\nEnter again:\n".encode()
                )
                continue

            break  # ✅ valid input

        with lock:
            rooms[room].append((conn, username))
            users[username] = {"conn": conn, "room": room}

        print(f"[JOIN] {username} joined {room}")
        conn.send((get_users() + "\n").encode())

        # ✅ MAIN LOOP
        while True:
            while b"\n" not in buffer:
                data = conn.recv(4096)
                if not data:
                    raise ConnectionError("Client disconnected")
                buffer += data

            line, buffer = buffer.split(b"\n", 1)
            message = line.decode(errors="ignore").strip()

            if len(message) > MAX_MSG_SIZE:
                conn.send("Message too large\n".encode())
                continue

            total_bytes += len(line)

            # PING
            if message == "PING":
                conn.send("PONG\n".encode())
                continue

            # USERS
            if message.startswith("/users"):
                conn.send((get_users() + "\n").encode())
                continue

            # PRIVATE MESSAGE
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

                with lock:
                    target_user = users.get(target)

                if target_user:
                    target_user["conn"].send(
                        f"[{timestamp}] {username} (private): {msg} (RTT: {rt} ms)\n".encode()
                    )
                    conn.send(f"[SENT to {target}]\n".encode())
                else:
                    conn.send("User not found\n".encode())

                continue

            # FILE TRANSFER
            if message.startswith("FILE"):
                parts = message.split()
                if len(parts) < 4:
                    continue

                target, filename, size = parts[1], parts[2], int(parts[3])

                file_data = b""

                if buffer:
                    take = min(len(buffer), size)
                    file_data += buffer[:take]
                    buffer = buffer[take:]

                if len(file_data) < size:
                    file_data += recv_exact(conn, size - len(file_data))

                total_bytes += len(file_data)

                with lock:
                    target_user = users.get(target)

                if target_user:
                    target_conn = target_user["conn"]
                    target_conn.send(f"FILE {username} {filename} {size}\n".encode())
                    target_conn.sendall(file_data)
                else:
                    conn.send("User not found\n".encode())

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

    except ConnectionError:
        print(f"[DISCONNECT] {addr}")
    except ssl.SSLError as e:
        print(f"[SSL ERROR] {e}")
    except Exception as e:
        print(f"[ERROR] {e}")

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
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((HOST, PORT))
    server.listen(5)

    print(f"[SUCCESS] Server running on {HOST}:{PORT}")
    print("Waiting for clients...\n")

    while True:
        client_socket, addr = server.accept()
        secure_socket = context.wrap_socket(client_socket, server_side=True)

        threading.Thread(
            target=handle_client,
            args=(secure_socket, addr),
            daemon=True
        ).start()


if __name__ == "__main__":
    start_server()
