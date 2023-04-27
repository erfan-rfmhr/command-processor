import asyncio
import os

import zmq
from dotenv import load_dotenv

load_dotenv()
DEFAULT_SERVER_ENDPOINT = "tcp://127.0.0.1:5555"


async def server():
    # Define the endpoint for the server
    server_endpoint = os.getenv("SERVER_ENDPOINT", DEFAULT_SERVER_ENDPOINT)

    # Create a ZMQ context and socket
    context = zmq.Context()
    socket = context.socket(zmq.REP)

    # Bind the socket to the endpoint
    socket.bind(server_endpoint)

    while True:
        # Wait for a request from the client
        request = socket.recv()

        # Process the request
        response = f"Server received request: {request.decode()}"
        print(response)

        # Send a response back to the client
        socket.send(response.encode())


async def main():
    await server()


if __name__ == "__main__":
    asyncio.run(main())
