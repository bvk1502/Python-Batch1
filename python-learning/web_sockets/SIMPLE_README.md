# Simple WebSocket Examples for Beginners

Welcome to WebSocket programming! These examples are designed to be easy to understand and run.

## �� Quick Start

### 1. Install Requirements
```bash
pip install websockets aioconsole
```

### 2. Run Your First WebSocket

**Terminal 1 - Start the server:**
```bash
python 01_simple_server.py
```

**Terminal 2 - Run the client:**
```bash
python 02_simple_client.py
```

## 📚 Examples Overview

### 1. Simple Echo (01_simple_server.py + 02_simple_client.py)
- **What it does**: Server echoes back any message it receives
- **Good for**: Understanding basic WebSocket communication
- **Key concept**: Send and receive messages

### 2. Chat Application (03_chat_server.py + 04_chat_client.py)
- **What it does**: Multiple clients can chat with each other
- **Good for**: Learning about broadcasting messages
- **Key concept**: Multiple clients, real-time communication

### 3. Shared Counter (05_counter_server.py + 06_counter_client.py)
- **What it does**: All clients share a counter that they can increment/reset
- **Good for**: Understanding shared state
- **Key concept**: Server maintains state, clients can modify it

## 🎯 How to Run Each Example

### Example 1: Echo Server
```bash
# Terminal 1
python 01_simple_server.py

# Terminal 2
python 02_simple_client.py
```

### Example 2: Chat
```bash
# Terminal 1
python 03_chat_server.py

# Terminal 2
python 04_chat_client.py

# Terminal 3 (optional - for more clients)
python 04_chat_client.py
```

### Example 3: Counter
```bash
# Terminal 1
python 05_counter_server.py

# Terminal 2
python 06_counter_client.py

# Terminal 3 (optional - for more clients)
python 06_counter_client.py
```

## 🔍 What You'll Learn

1. **Basic WebSocket Connection**: How clients connect to servers
2. **Message Passing**: How to send and receive messages
3. **Multiple Clients**: How servers handle multiple connections
4. **Real-time Communication**: Instant message delivery
5. **Shared State**: How multiple clients can interact with shared data

## 🐛 Troubleshooting

### "Connection Refused" Error
- Make sure the server is running before the client
- Check that you're using the correct port (8765)

### "Module Not Found" Error
- Run: `pip install websockets aioconsole`

### Server Won't Start
- Make sure no other program is using port 8765
- Try a different port by changing the number in the code

## 🎉 Next Steps

After running these examples, try:
1. Modifying the messages
2. Adding new commands
3. Creating your own WebSocket application
4. Reading the main README.md for advanced features

---

**Happy WebSocket Programming! ��** 