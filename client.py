import asyncio
import os
import sys
from dotenv import load_dotenv
import zmq

load_dotenv()
DEFAULT_JSON_FILE = "command.json"
DEFAULT_SERVER_ENDPOINT = "tcp://localhost:5555"


async def client():
    # Define the endpoint for the server
    server_endpoint = os.getenv("SERVER_ENDPOINT" or DEFAULT_SERVER_ENDPOINT)

    # Create a ZMQ context and socket
    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    # Connect the socket to the endpoint
    socket.connect(server_endpoint)

    # Load the JSON request from a file
    try:
        json_file = sys.argv[1]
    except IndexError:
        json_file = DEFAULT_JSON_FILE

    try:
        with open(json_file, "r") as reader:
            request = reader.read()
    except FileNotFoundError:
        print(f"File not found: {json_file}")
        sys.exit(2)

    # Send a request to the server
    socket.send(request.encode())

    # Wait for a response from the server
    response = socket.recv()
    print(f"Received response from server: {response.decode()}")


async def main():
    await client()


if __name__ == "__main__":
    asyncio.run(main())
