import socket
import ssl
import threading
from datetime import datetime

HOST = "0.0.0.0"
PORT = 6000
ROOM_LIMIT = 10

rooms = {
    "AI": [],
    "CN": [],
    "ML": []
}

users = {}  # username → {conn, room}
lock = threading.Lock()


def get_room_info():
    info = "Rooms:\n"
    for room in rooms:
        info += f"{room}: {len(rooms[room])}/{ROOM_LIMIT}\n"
    return info


def get_all_users():
    info = "\nActive Users:\n"
    for room in rooms:
        names = [u for _, u in rooms[room]]
        info += f"{room}: {', '.join(names) if names else 'None'}\n"
    return info


def broadcast(room, message):
    for client, user in rooms[room][:]:
        try:
            client.send((message + "\n").encode())
        except:
            rooms[room].remove((client, user))


def handle_client(conn, addr):
    print("Client connected:", addr)

    username = None
    room = None

    try:
        conn.send((get_room_info() + "\n").encode())

        data = conn.recv(1024).decode().strip()
        parts = data.split()

        if len(parts) < 3 or parts[0] != "JOIN":
            conn.send("Invalid JOIN format\n".encode())
            return

        username, room = parts[1], parts[2]

        with lock:
            if room not in rooms:
                conn.send("Invalid room\n".encode())
                return

            if len(rooms[room]) >= ROOM_LIMIT:
                conn.send("Room full\n".encode())
                return

            rooms[room].append((conn, username))
            users[username] = {"conn": conn, "room": room}

        print(f"{username} joined {room}")
        conn.send((get_all_users() + "\n").encode())

        while True:
            message = conn.recv(1024).decode().strip()

            if not message:
                break

            # LATENCY
            if message == "PING":
                conn.send("PONG\n".encode())
                continue

            # USER LIST
            if message == "/users":
                conn.send((get_all_users() + "\n").encode())
                continue

            # PRIVATE MESSAGE
            if message.startswith("/msg"):
                parts = message.split(" ", 2)

                if len(parts) < 3:
                    conn.send("Usage: /msg username message\n".encode())
                    continue

                target, msg = parts[1], parts[2]
                timestamp = datetime.now().strftime("%H:%M:%S")

                full_msg = f"[{timestamp}] {username} (private): {msg}"

                if target in users:
                    users[target]["conn"].send((full_msg + "\n").encode())
                    conn.send(f"[SENT to {target}]\n".encode())
                else:
                    conn.send("User not found\n".encode())

                continue

            # FILE TRANSFER
            if message.startswith("/sendfile"):
                parts = message.split()

                if len(parts) < 3:
                    conn.send("Usage: /sendfile username filename\n".encode())
                    continue

                target, filename = parts[1], parts[2]

                if target not in users:
                    conn.send("User not found\n".encode())
                    continue

                try:
                    with open(filename, "rb") as f:
                        data = f.read()

                    header = f"FILE {username} {filename} {len(data)}\n"
                    users[target]["conn"].send(header.encode())
                    users[target]["conn"].send(data)

                    conn.send(f"[FILE SENT to {target}]\n".encode())

                except:
                    conn.send("File error\n".encode())

                continue

            # EXIT
            if message == "/exit":
                break

            # NORMAL CHAT
            timestamp = datetime.now().strftime("%H:%M:%S")
            full_message = f"[{timestamp}] {username}: {message}"

            print(full_message)
            broadcast(room, full_message)

    except Exception as e:
        print("Error:", e)
import socket
import ssl
import threading
from datetime import datetime

HOST = "0.0.0.0"
PORT = 6000
ROOM_LIMIT = 10

rooms = {
    "AI": [],
    "CN": [],
    "ML": []
}

users = {}  # username → {conn, room}
lock = threading.Lock()


def get_room_info():
    info = "Rooms:\n"
    for room in rooms:
        info += f"{room}: {len(rooms[room])}/{ROOM_LIMIT}\n"
    return info


def get_all_users():
    info = "\nActive Users:\n"
    for room in rooms:
        names = [u for _, u in rooms[room]]
        info += f"{room}: {', '.join(names) if names else 'None'}\n"
    return info


def broadcast(room, message):
    for client, user in rooms[room][:]:
        try:
            client.send((message + "\n").encode())
        except:
            rooms[room].remove((client, user))


def handle_client(conn, addr):
    print("Client connected:", addr)

    username = None
    room = None

    try:
        conn.send((get_room_info() + "\n").encode())



                conn.send("Invalid room\n".encode())
                conn.send("Room full\n".encode())
                return
            users[username] = {"conn": conn, "room": room}
        print(f"{username} joined {room}")
        conn.send((get_all_users() + "\n").encode())
        while True:
            message = conn.recv(1024).decode().strip()
            if not message:
                break

            # LATENCY
            if message == "PING":
                conn.send("PONG\n".encode())
                continue

                conn.send((get_all_users() + "\n").encode())

            # PRIVATE MESSAGE
                parts = message.split(" ", 2)

                    conn.send("Usage: /msg username message\n".encode())
                    continue

                target, msg = parts[1], parts[2]
                timestamp = datetime.now().strftime("%H:%M:%S")

                full_msg = f"[{timestamp}] {username} (private): {msg}"

                if target in users:
                    users[target]["conn"].send((full_msg + "\n").encode())
                    conn.send(f"[SENT to {target}]\n".encode())
                else:
                    conn.send("User not found\n".encode())

                continue

            # FILE TRANSFER
            if message.startswith("/sendfile"):
                parts = message.split()

                if len(parts) < 3:
                    conn.send("Usage: /sendfile username filename\n".encode())
                    continue

                target, filename = parts[1], parts[2]

            args=(secure_socket, addr),
            daemon=True
        ).start()
if __name__ == "__main__":
    start_server()

        threading.Thread(
            target=handle_client,

        client_socket, addr = server.accept()
        secure_socket = context.wrap_socket(client_socket, server_side=True)
    while True:


    print("Secure Chat Server Running on port 6000")
                if target not in users:
    server.bind((HOST, PORT))
    server.listen(5)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    conn.send("User not found\n".encode())


def start_server():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain("server.crt", "server.key")
    except Exception as e:

            if username in users:
        print(f"{username} disconnected")
        conn.close()
                del users[username]

            if room:
                rooms[room] = [(c, u) for c, u in rooms[room] if c != conn]

        broadcast(room, f"{username} left the chat")
    finally:
        with lock:
        print("Error:", e)
            broadcast(room, full_message)


            print(full_message)
                    continue
            full_message = f"[{timestamp}] {username}: {message}"
            # NORMAL CHAT
            timestamp = datetime.now().strftime("%H:%M:%S")

                break

                    conn.send("File error\n".encode())
            if message == "/exit":

            # EXIT

                continue
                except:
                try:


                    conn.send(f"[FILE SENT to {target}]\n".encode())
                    users[target]["conn"].send(header.encode())
                    users[target]["conn"].send(data)
                    with open(filename, "rb") as f:
                        data = f.read()

                    header = f"FILE {username} {filename} {len(data)}\n"
                if len(parts) < 3:
            if message.startswith("/msg"):
                continue
            # USER LIST
            if message == "/users":



            rooms[room].append((conn, username))

            if len(rooms[room]) >= ROOM_LIMIT:

                return
            if room not in rooms:
        with lock:
        username, room = parts[1], parts[2]
        if len(parts) < 3 or parts[0] != "JOIN":
            return
            conn.send("Invalid JOIN format\n".encode())
        data = conn.recv(1024).decode().strip()

