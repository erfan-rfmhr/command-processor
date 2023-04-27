import asyncio
import os
import sys

import zmq


async def client():
    # Define the endpoint for the server
    server_endpoint = os.getenv("SERVER_ENDPOINT", "tcp://localhost:5555")

    # Create a ZMQ context and socket
    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    # Connect the socket to the endpoint
    socket.connect(server_endpoint)

    # Load the JSON request from a file
    json_file = sys.argv[1]
    with open(json_file, "r") as reader:
        request = reader.read()

    # Send a request to the server
    socket.send(request.encode())

    # Wait for a response from the server
    response = socket.recv()
    print(f"Received response from server: {response.decode()}")


async def main():
    await client()


if __name__ == "__main__":
    asyncio.run(main())
