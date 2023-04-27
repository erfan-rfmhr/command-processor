import zmq

import os


async def client():
    # Define the endpoint for the server
    server_endpoint = os.getenv("SERVER_ENDPOINT", "tcp://localhost:5555")

    # Create a ZMQ context and socket
    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    # Connect the socket to the endpoint
    socket.connect(server_endpoint)

    # Send a request to the server
    request = "Hello from client!"
    socket.send(request.encode())

    # Wait for a response from the server
    response = socket.recv()
    print(f"Received response from server: {response.decode()}")
