"""
Simple Chat Client - Beginner Example
Interactive chat client that can send and receive messages
"""

import asyncio
import websockets
import aioconsole

async def chat_client():
    """Interactive chat client"""
    server_url = "ws://localhost:8765"
    
    try:
        print("Connecting to chat server...")
        
        async with websockets.connect(server_url) as websocket:
            print("Connected to chat server!")
            
            # Get user's name
            name = await aioconsole.ainput("Enter your name: ")
            
            # Create two tasks: one for sending, one for receiving
            async def receive_messages():
                """Receive and display messages"""
                try:
                    async for message in websocket:
                        print(f"\n{message}")
                        print(f"{name}: ", end="", flush=True)
                except:
                    print("\nConnection lost!")
            
            async def send_messages():
                """Send user messages"""
                try:
                    while True:
                        message = await aioconsole.ainput(f"{name}: ")
                        if message.lower() in ['quit', 'exit', 'bye']:
                            break
                        await websocket.send(message)
                except:
                    pass
            
            # Run both tasks at the same time
            receive_task = asyncio.create_task(receive_messages())
            send_task = asyncio.create_task(send_messages())
            
            # Wait for either task to finish
            done, pending = await asyncio.wait(
                [receive_task, send_task],
                return_when=asyncio.FIRST_COMPLETED
            )
            
            # Cancel the other task
            for task in pending:
                task.cancel()
                
    except websockets.exceptions.ConnectionRefused:
        print("❌ Could not connect to chat server!")
        print("Make sure the server is running: python 03_chat_server.py")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(chat_client())
```

```
