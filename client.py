import asyncio
import json
import os
import sys
from pprint import pprint

import zmq
from dotenv import load_dotenv

load_dotenv()
DEFAULT_JSON_FILE = "command.json"
DEFAULT_SERVER_ENDPOINT = "tcp://127.0.0.1:5555"


def format_response(given_command_type: str, command_dict: dict, execution_result: str) -> dict:
    """Format the response to be sent back to the client."""
    math_expression = command_dict.get("expression", None)
    output = {
        given_command_type: command_dict.get('command_name', math_expression) + " " + " ".join(
            command_dict.get("parameters", [])),
        "result": execution_result
    }
    return output


async def client():
    """Send a request to the server and print the response.
    The request is loaded from a JSON file.

    os commands response format: {given_os_command: <command>, result: <result>}

    compute commands response format: {given_math_expression: <expression>, result: <result>}"""

    # Define the endpoint for the server
    server_endpoint = os.getenv("SERVER_ENDPOINT", DEFAULT_SERVER_ENDPOINT)

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
    # Decode the response and convert request to a dictionary
    execution_result = response.decode()
    # Check if the command type is valid
    if execution_result == "Invalid command type" or execution_result == "Invalid request format":
        print(execution_result)
        print("Please check the command type and format of the request.")
        print("The request should be in the following format:")
        print("{command_type: <os>, command_name: <command_name>, parameters: <parameters>}")
        print("{command_type: <compute>, expression: <expression>}")
        sys.exit(2)

    command_dict = json.loads(request)
    # Format the response
    if command_dict["command_type"] == "compute":
        output = format_response("given_math_expression", command_dict, execution_result)
    else:
        output = format_response("given_os_command", command_dict, execution_result)
    pprint(output, indent=4)


async def main():
    await client()


if __name__ == "__main__":
    asyncio.run(main())
