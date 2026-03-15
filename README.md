# Secure Multi-Room Chat System with File Transfer (SSL/TLS)

## Overview

This project implements a secure multi-client chat system using low-level TCP socket programming with SSL/TLS encryption. The system supports multiple concurrent clients, room-based communication, message timestamps, and secure file transfer between clients.

The application demonstrates important Computer Networks concepts such as:

- TCP socket communication
- Secure communication using SSL/TLS
- Client–server architecture
- Concurrency using threads
- Application-layer protocol design

---

## Features

### Secure Communication
All communication between clients and server is encrypted using SSL/TLS sockets.

### Multi-Client Support
The server supports multiple clients simultaneously using threading.

### Room-Based Chat
Users can join predefined rooms:

- AI
- CN
- ML

Messages are broadcast only to users within the same room.

### Username Validation
Usernames must follow these rules:

- Only letters, numbers, and underscores allowed
- No special characters

Example valid usernames:

Alice_1  
Bob2  
user_name  

Example invalid usernames:

Alice!  
Bob@  
user#1  

---

### Message Timestamps
All chat messages include timestamps.

Example:

[14:32:10] Alice_1: Hello everyone

---

### Secure File Transfer
Clients can send files using the command:

/sendfile filename

Files are transmitted through the TLS encrypted socket connection and broadcast to users in the same room.

Example:

/sendfile test.txt

---

## Project Architecture

The system follows a Client–Server Architecture.
         +--------------------+
         |      SERVER        |
         |--------------------|
         | SSL/TLS Encryption |
         | Room Management    |
         | Thread Handling    |
         +---------+----------+
                   |
   -------------------------------------
   |                 |                 |
Client 1 Client 2 Client 3 (AI) (AI) (CN)

Communication flow:

Client → TLS → Server → Broadcast to Room Members

---

## Technologies Used

- Python
- TCP Sockets
- SSL/TLS
- Threading
- Git & GitHub

---

## Folder Structure
cn_secure_chat
│
├── client
│ └── client.py
│
├── server
│ ├── server.py
│ ├── server.crt
│ └── server.key
│
├── security
│ ├── server.crt
│ └── server.key
│
├── README.md
└── .gitignore

---

## How to Run the Project

### 1. Start the Server

Open a terminal and run:

cd server  
python server.py

Expected output:

Secure Chat Server Running on port 6000

---

### 2. Start Client

Open another terminal and run:

cd client  
python client.py

Example:

Enter username: Alice_1  
Choose room: AI  

---

### 3. Start Multiple Clients

Run the client in multiple terminals:

python client.py

Users can then chat in the same room.

---

## Example Chat

Client 1 sends:

Hello everyone

Client 2 receives:

[14:32:10] Alice_1: Hello everyone

---

## File Transfer

Create a test file in the client directory:

echo Hello CN Project > test.txt

Send file:

/sendfile test.txt

Receiving clients will see:

Receiving file test.txt  
File received successfully

---

## Security Implementation

The project uses SSL/TLS encryption to secure communication.

Server loads certificate and key:

server.crt  
server.key  

All socket communication is wrapped using TLS:

SSL → TCP Socket → Application Protocol

---

## Application Protocol Design

Custom protocol messages:

JOIN username room  
MESSAGE text  
FILE filename filesize  

Example:

JOIN Alice_1 AI  
FILE test.txt 1024  

---

## Future Improvements

Potential extensions include:

- Private messaging (/msg username)
- User list command (/users)
- Message history
- GUI interface (Tkinter or Web UI)
- File transfer progress indicator
- Authentication system

---

## Learning Outcomes

This project demonstrates understanding of:

- Socket programming
- Secure network communication
- Concurrency in network servers
- Protocol design
- Client-server architectures

---

## Author

Computer Networks Project  
Secure Chat System with SSL/TLS
