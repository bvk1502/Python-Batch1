"""
Counter Client - Beginner Example
Client that can increment and reset a shared counter
"""

import asyncio
import websockets
import aioconsole

async def counter_client():
    """Interactive counter client"""
    server_url = "ws://localhost:8765"
    
    try:
        print("Connecting to counter server...")
        
        async with websockets.connect(server_url) as websocket:
            print("Connected to counter server!")
            print("Commands: 'increment', 'reset', 'quit'")
            
            # Create two tasks: one for receiving, one for sending
            async def receive_messages():
                """Receive and display messages"""
                try:
                    async for message in websocket:
                        print(f"\n{message}")
                        print("Command: ", end="", flush=True)
                except:
                    print("\nConnection lost!")
            
            async def send_commands():
                """Send user commands"""
                try:
                    while True:
                        command = await aioconsole.ainput("Command: ")
                        if command.lower() in ['quit', 'exit']:
                            break
                        await websocket.send(command)
                except:
                    pass
            
            # Run both tasks at the same time
            receive_task = asyncio.create_task(receive_messages())
            send_task = asyncio.create_task(send_commands())
            
            # Wait for either task to finish
            done, pending = await asyncio.wait(
                [receive_task, send_task],
                return_when=asyncio.FIRST_COMPLETED
            )
            
            # Cancel the other task
            for task in pending:
                task.cancel()
                
    except websockets.exceptions.ConnectionRefused:
        print("❌ Could not connect to counter server!")
        print("Make sure the server is running: python 05_counter_server.py")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(counter_client())
