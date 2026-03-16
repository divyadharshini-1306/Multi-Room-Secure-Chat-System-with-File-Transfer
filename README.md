# Secure Multi-Room Chat System with File Transfer (SSL/TLS)

## Overview

This project implements a **secure multi-client chat system** using low-level **TCP socket programming with SSL/TLS encryption**. The system supports **multiple concurrent clients, room-based communication, message timestamps, and secure file transfer between clients**.

Clients can connect **from different devices on the same network (LAN/WiFi)** by using the server's IP address.

The project demonstrates important **Computer Networks concepts**, including:

* TCP socket communication
* Secure communication using SSL/TLS
* Client–server architecture
* Concurrency using threads
* Application-layer protocol design
* Multi-device communication over LAN

---

## Features

### Secure Communication

All communication between clients and server is **encrypted using SSL/TLS sockets**, ensuring privacy and preventing eavesdropping.

### Multi-Client Support

The server supports **multiple clients simultaneously** using **threading**, allowing many users to connect at the same time.

### Multi-Device Communication

Clients can connect from **different devices on the same WiFi/LAN network** by entering the **server's local IP address**.

### Room-Based Chat

Users can join predefined chat rooms:

* AI
* CN
* ML

Messages are **broadcast only to users in the same room**.

### Username Validation

Usernames must follow these rules:

* Only **letters**
* **Numbers**
* **Underscores**

Valid examples:

```
Alice_1
Bob2
user_name
```

Invalid examples:

```
Alice!
Bob@
user#1
```

### Message Timestamps

All messages include timestamps.

Example:

```
[14:32:10] Alice_1: Hello everyone
```

### Secure File Transfer

Clients can send files using:

```
/sendfile filename
```

Example:

```
/sendfile test.txt
```

Files are transmitted through the **TLS encrypted socket connection**.

---

## Project Architecture

The system follows a **Client–Server Architecture**.

```
          +--------------------+
          |       SERVER       |
          |--------------------|
          | SSL/TLS Encryption |
          | Room Management    |
          | Thread Handling    |
          +---------+----------+
                    |
     -----------------------------------
     |                |                |
   Client 1         Client 2         Client 3
     (AI)             (AI)             (CN)
```

Communication flow:

```
Client → TLS → Server → Broadcast to Room Members
```

---

## Technologies Used

| Component            | Technology  |
| -------------------- | ----------- |
| Programming Language | Python      |
| Networking           | TCP Sockets |
| Security             | SSL/TLS     |
| Concurrency          | Threading   |
| Version Control      | Git         |
| Repository Hosting   | GitHub      |

---

## Folder Structure

```
cn_secure_chat
│
├── client
│   └── client.py
│
├── server
│   ├── server.py
│   ├── server.crt
│   └── server.key
│
├── security
│   ├── server.crt
│   └── server.key
│
├── README.md
└── .gitignore
```

---

## How to Run the Project

### 1. Start the Server

Open a terminal on the **server machine**.

Navigate to the server directory:

```
cd server
```

Run the server:

```
python server.py
```

Expected output:

```
Secure Chat Server Running on port 6000
```

The server listens for incoming client connections.

---

### 2. Find the Server IP Address

To allow clients from other devices to connect, find the **server's local IP address**.

#### Windows

```
ipconfig
```

Look for:

```
IPv4 Address : 10.1.21.132
```

#### Linux / Mac

```
ifconfig
```

or

```
ip addr
```

Example:

```
192.168.1.15
```

This IP address will be used by clients to connect to the server.

---

### 3. Start a Client

Open a new terminal.

Navigate to the client folder:

```
cd client
```

Run the client:

```
python client.py
```

The program will ask for the server IP:

```
Enter server IP address:
```

Example:

```
10.1.21.132
```

---

### 4. Enter Username

Example:

```
Enter username: Alice
```

---

### 5. Choose a Room

```
Available rooms: ['AI', 'CN', 'ML']
Choose a room: AI
```

---

### 6. Start Multiple Clients

Run the client on **multiple terminals or different devices**.

Example users:

```
Alice (AI room)
Bob (AI room)
Charlie (CN room)
```

Users in the **same room** can communicate.

---

## Example Chat

Client 1 sends:

```
Hello everyone
```

Client 2 receives:

```

---
## File Transfer Example

Create a test file:

echo Hello CN Project > test.txt
```
Send the file:

```
/sendfile test.txt

Server response:
```
File test.txt received

The received file will be saved as:
```
received_test.txt
```

---

## Security Implementation
The system uses **SSL/TLS encryption** to secure communication.

The server loads a certificate and private key:

```
server.key
```


```
SSL/TLS → TCP Socket → Application Protocol
```

This ensures:

* Protection from packet sniffing
* Secure data transmission

---

## Application Protocol Design

Custom protocol messages used by the system:

```
JOIN username room
MESSAGE text
FILE filename filesize
```

Example:

```
JOIN Alice AI
FILE test.txt 1024
```

This protocol allows the server to identify **user actions and message types**.

---

## Future Improvements

Possible extensions include:

* Private messaging (`/msg username`)
* User list command (`/users`)
* Message history storage
* GUI interface (Tkinter or Web UI)
* File transfer progress indicator
* User authentication system

---

## Learning Outcomes

This project demonstrates understanding of:

* Socket programming
* Secure network communication
* Multi-client concurrency
* Client–server architectures
* Protocol design
* LAN-based multi-device communication

---

## Author

Computer Networks Project
Secure Multi-Room Chat System with SSL/TLS
* Encrypted communication
All socket communication is wrapped using TLS:
server.crt


```

```

```


