import asyncio
import os
import json
import zmq
from dotenv import load_dotenv

load_dotenv()
DEFAULT_SERVER_ENDPOINT = "tcp://127.0.0.1:5555"


async def systemic_processing(command_name: str, parameters: list) -> str:
    """Perform some systemic processing on the command."""
    proc = await asyncio.create_subprocess_exec(command_name, *parameters, stdout=asyncio.subprocess.PIPE,
                                                stderr=asyncio.subprocess.PIPE)
    await proc.wait()
    result = await proc.stdout.read()

    # If the result is empty, then there was an error
    if result == b'':
        result = await proc.stderr.read()

    return result.decode()


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
        data = json.loads(request.decode())
        response = await systemic_processing(data["command_name"], data["parameters"])

        # Send a response back to the client
        socket.send(response.encode())


async def main():
    await server()


if __name__ == "__main__":
    asyncio.run(main())
