"""
Counter Server - Beginner Example
Server that keeps a counter and sends updates to all clients
"""

import asyncio
import websockets

# Keep track of connected clients and counter
connected_clients = []
counter = 0

async def counter_handler(websocket, path):
    """Handle counter client connections"""
    global counter
    
    # Add this client to our list
    connected_clients.append(websocket)
    client_id = len(connected_clients)
    
    print(f"Client {client_id} connected! Total clients: {len(connected_clients)}")
    
    # Send current counter value to new client
    await websocket.send(f"Current counter: {counter}")
    
    try:
        # Listen for messages from this client
        async for message in websocket:
            print(f"Client {client_id} sent: {message}")
            
            if message.lower() == "increment":
                counter += 1
                print(f"Counter incremented to: {counter}")
                
                # Send new counter value to all clients
                for client in connected_clients:
                    try:
                        await client.send(f"Counter: {counter}")
                    except:
                        connected_clients.remove(client)
                        
            elif message.lower() == "reset":
                counter = 0
                print("Counter reset to 0")
                
                # Send reset message to all clients
                for client in connected_clients:
                    try:
                        await client.send("Counter reset to 0")
                    except:
                        connected_clients.remove(client)
                        
    except websockets.exceptions.ConnectionClosed:
        print(f"Client {client_id} disconnected!")
    finally:
        if websocket in connected_clients:
            connected_clients.remove(websocket)
        print(f"Client {client_id} left. Total clients: {len(connected_clients)}")

async def main():
    """Start the counter server"""
    print("Starting Counter Server...")
    print("Server will run on: ws://localhost:8765")
    print("Clients can send 'increment' or 'reset' messages")
    print("Press Ctrl+C to stop the server")
    
    server = await websockets.serve(counter_handler, "localhost", 8765)
    await server.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped!") 