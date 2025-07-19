"""
Simple Chat Server - Beginner Example
Multiple clients can connect and chat with each other
"""

import asyncio
import websockets

# Keep track of all connected clients
connected_clients = []

async def chat_handler(websocket, path):
    """Handle chat client connections"""
    # Add this client to our list
    connected_clients.append(websocket)
    client_id = len(connected_clients)
    
    print(f"Client {client_id} connected! Total clients: {len(connected_clients)}")
    
    try:
        # Send welcome message
        welcome = f"Welcome! You are client {client_id}"
        await websocket.send(welcome)
        
        # Listen for messages from this client
        async for message in websocket:
            print(f"Client {client_id}: {message}")
            
            # Send message to all other clients
            for client in connected_clients:
                if client != websocket:  # Don't send back to sender
                    try:
                        await client.send(f"Client {client_id}: {message}")
                    except:
                        # Remove disconnected clients
                        connected_clients.remove(client)
                        
    except websockets.exceptions.ConnectionClosed:
        print(f"Client {client_id} disconnected!")
    finally:
        # Remove client when they disconnect
        if websocket in connected_clients:
            connected_clients.remove(websocket)
        print(f"Client {client_id} left. Total clients: {len(connected_clients)}")

async def main():
    """Start the chat server"""
    print("Starting Chat Server...")
    print("Server will run on: ws://localhost:8765")
    print("Multiple clients can connect and chat!")
    print("Press Ctrl+C to stop the server")
    
    server = await websockets.serve(chat_handler, "localhost", 8765)
    await server.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped!") 