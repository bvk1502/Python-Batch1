"""
Simple WebSocket Server - Beginner Example
This server just echoes back any message it receives
"""

import asyncio
import websockets

async def echo_handler(websocket):
    """Simple handler that echoes back messages"""
    print("New client connected!")
    
    try:
        # Listen for messages from the client
        async for message in websocket:
            print(f"Received: {message}")
            
            # Send the message back to the client
            response = f"Server received: {message}"
            await websocket.send(response)
            print(f"Sent back: {response}")
            
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected!")

async def main():
    """Start the WebSocket server"""
    print("Starting WebSocket server...")
    print("Server will run on: ws://localhost:8765")
    print("Press Ctrl+C to stop the server")
    
    # Start the server
    server = await websockets.serve(echo_handler, "localhost", 8765)
    
    # Keep the server running
    await server.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped!") 