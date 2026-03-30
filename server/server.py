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

def get_room_info():
    info = "Available Rooms:\n"
    for room in rooms:
        info += f"{room} → {len(rooms[room])}/{ROOM_LIMIT} users\n"
    return info


def broadcast(room, message, sender):
    for client, user in rooms[room][:]:
        if client != sender:
            try:
                client.send(message.encode())
            except:
                rooms[room].remove((client, user))


def handle_client(conn, addr):

    print("Client connected:", addr)

    room = None
    username = None
    private_target = None

    try:
        # Send room info
        conn.send(get_room_info().encode())

        data = conn.recv(1024).decode()
        parts = data.split()

        if parts[0] == "JOIN":
            username = parts[1]
            room = parts[2]

        if len(rooms[room]) >= ROOM_LIMIT:
            conn.send(f"Room {room} is full".encode())
            conn.close()
            return

        print(f"{username} joined {room}")

        rooms[room].append((conn, username))

        while True:

            try:
                message = conn.recv(1024)
                if not message:
                    break
            except:
                break

            message = message.decode()

            # 🔥 PRIVATE CHAT
            if message.startswith("/msg"):
                parts = message.split()

                if len(parts) < 2:
                    conn.send("Usage: /msg <username>".encode())
                    continue

                target_name = parts[1]

                found = False
                for client, user in rooms[room]:
                    if user == target_name:
                        private_target = (client, user)
                        conn.send(f"Private chat started with {user}".encode())
                        found = True
                        break

                if not found:
                    conn.send("User not found".encode())

                continue

            # 🔥 EXIT PRIVATE
            if message.strip() == "/leave_private":
                private_target = None
                conn.send("Exited private chat".encode())
                continue

            # 🔥 PRIVATE MESSAGE MODE
            if private_target:
                target_conn, target_user = private_target
                timestamp = datetime.now().strftime("%H:%M:%S")

                private_msg = f"[{timestamp}] {username} (private): {message}"

                try:
                    target_conn.send(private_msg.encode())
                except:
                    conn.send("User disconnected".encode())

                continue

            # 🔹 NORMAL ROOM CHAT
            timestamp = datetime.now().strftime("%H:%M:%S")
            full_message = f"[{timestamp}] {username}: {message}"

            print(full_message)
            broadcast(room, full_message, conn)

    except Exception as e:
        print("Error:", e)

    finally:
        # 🔥 REMOVE USER CLEANLY
        if room:
            rooms[room] = [(c, u) for c, u in rooms[room] if c != conn]

        print(f"{username} disconnected")
        conn.close()


def start_server():

    print("Starting server...")

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain("server.crt", "server.key")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((HOST, PORT))
    server.listen(5)

    print("Secure Chat Server Running on port 6000")

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
