# 🔐 Secure Multi-Room Chat System with File Transfer (SSL/TLS)

## 📌 Overview

This project implements a **secure multi-client chat system** using **TCP socket programming with SSL/TLS encryption**.

It supports:
- Real-time communication
- Room-based messaging
- Cross-room private chat
- Secure file transfer
- Performance metrics (latency, RTT, throughput)

Multiple clients can connect from different devices over the same **LAN/WiFi network**.

---

## 🚀 Key Features

### 🔒 Secure Communication
- Uses **SSL/TLS encryption**
- Prevents unauthorized access and packet sniffing

---

### 👥 Multi-Client Support
- Multiple clients can connect simultaneously
- Implemented using **threading**

---

### 🌐 Multi-Device Connectivity
- Clients can connect from different systems using server IP

---

### 🧠 Room-Based Chat
Users can join predefined rooms:
- `AI`
- `CN`
- `ML`

Messages are broadcast only within the selected room.

---

### 💬 Private Messaging (Cross-Room)
Send direct messages to any user:

```bash /msg username message
📁 Secure File Transfer

Send files between clients:

/sendfile username filename

✔ Chunk-based transfer (prevents corruption)
✔ Works across rooms
✔ Received file is saved as:

received_<filename>
📝 File Creation (Important)

Files can be created locally before sending using terminal:

echo Hello CN Project > test.txt

Then send using:

/sendfile username test.txt
📊 Performance Metrics
🔹 Latency

Measured using:

/ping

Output:

Latency: 10 ms
🔹 Response Time (RTT)

Displayed with each message:

[18:45:12] Divya13: hello (RTT: 0.53 ms)
🔹 Throughput

Server calculates data transfer rate:

[PERFORMANCE] Throughput: 120.45 KB/s
📡 Active User Tracking
/users

Example:

Active Users:
AI: Divya13, fatima12
CN: None
ML: None
🧾 Username Validation

Usernames must contain only:

Letters (A–Z, a–z)
Numbers (0–9)
Underscore (_)
🕒 Timestamped Messages

All messages include timestamps:

[19:52:28] Divya13: hello everyone (RTT: 0.53 ms)
🏗️ System Architecture
          +----------------------+
          |        SERVER        |
          |----------------------|
          |  SSL/TLS Encryption  |
          |  Room Management     |
          |  User Tracking       |
          |  Thread Handling     |
          +----------+-----------+
                     |
      ----------------------------------
      |               |               |
   Client 1        Client 2        Client 3
     (AI)            (AI)            (CN)
⚙️ Technologies Used
Component	Technology
Language	Python
Networking	TCP Sockets
Security	SSL/TLS
Concurrency	Threading
Version Control	Git
📁 Project Structure
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
▶️ How to Run
1️⃣ Start Server
cd server
python server.py
2️⃣ Get Server IP
ipconfig   # Windows
ifconfig   # Linux/Mac

Example:

192.168.0.104
3️⃣ Start Client
cd client
python client.py
4️⃣ Join Chat
Enter server IP: 192.168.0.104
Enter username: Divya13
Choose room: AI
💡 Commands
Command	Description
hello	Broadcast message
/msg user message	Private message
/users	View active users
/sendfile user file.txt	Send file
/ping	Check latency
/exit	Leave chat
📂 File Transfer Example
echo Hello CN > demo.txt
/sendfile fatima12 demo.txt

Receiver:

Receiving 'demo.txt' from Divya13...
Saved as received_demo.txt
🔐 Security Implementation
Uses SSL/TLS encryption
Server uses:
server.crt
server.key
📡 Application Protocol

Custom protocol used:

JOIN username room
/msg username message||timestamp
FILE username filename size
PING
📊 Performance Evaluation
🔹 Latency
Measured using /ping
Typical LAN latency: 5–20 ms
🔹 Response Time
Measured using timestamp-based RTT
Observed: <1 ms to 10 ms (LAN)
🔹 Throughput
Based on total data transferred per time
Observed during file transfer: 100–300 KB/s
🔹 Scalability
Thread-per-client model
Works efficiently for small to medium scale (10–50 clients)
Can be improved using async I/O for large-scale systems
🔧 Optimization and Fixes
Fixed file transfer corruption using chunk-based transfer
Resolved incorrect latency calculation
Improved RTT precision
Fixed /users command parsing bug
Handled client disconnections safely
Improved protocol stability
🧠 Learning Outcomes
Socket programming
Secure communication (SSL/TLS)
Multi-client concurrency
Client-server architecture
Protocol design
Performance evaluation
