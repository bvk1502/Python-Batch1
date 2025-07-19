"""
Simple WebSocket Client - Beginner Example
This client connects to the server and sends a few test messages
"""

import asyncio
import websockets

async def simple_client():
    """Simple WebSocket client"""
    # Server address
    server_url = "ws://localhost:8765"
    
    try:
        print("Connecting to WebSocket server...")
        
        # Connect to the server
        async with websockets.connect(server_url) as websocket:
            print("Connected successfully!")
            
            # Send some test messages
            test_messages = [
                "Hello, WebSocket!",
                "This is my second message",
                "Goodbye!"
            ]
            
            for message in test_messages:
                print(f"\nSending: {message}")
                
                # Send message to server
                await websocket.send(message)
                
                # Wait for response
                response = await websocket.recv()
                print(f"Received: {response}")
                
                # Small delay between messages
                await asyncio.sleep(1)
                
    except websockets.exceptions.ConnectionRefused:
        print("❌ Could not connect to server!")
        print("Make sure the server is running: python 01_simple_server.py")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(simple_client())
