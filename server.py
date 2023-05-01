import asyncio
import json
import os

import zmq
from dotenv import load_dotenv

from logger import get_logger
from utils import systemic_processing, computational_command_processing

load_dotenv()
DEFAULT_SERVER_ENDPOINT = "tcp://127.0.0.1:5555"


async def server():
    error_logger = get_logger()
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
        try:
            data = json.loads(request.decode())
            if data["command_type"] == "os":
                response = await systemic_processing(data["command_name"], data["parameters"])
            elif data["command_type"] == "compute":
                response = await computational_command_processing(data["expression"])
            else:
                response = "Invalid command type"
        # If the request is not in JSON format or if the request is missing a key
        except (json.JSONDecodeError, KeyError):
            response = "Invalid request format"
            error_logger.error(response)

        # Send a response back to the client
        socket.send(response.encode())


async def main():
    await server()


if __name__ == "__main__":
    asyncio.run(main())
