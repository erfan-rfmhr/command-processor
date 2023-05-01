import asyncio
import json
import os
from logger import get_logger
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


async def computational_command_processing(expression: str) -> str:
    result = eval(expression)
    return str(result)


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
