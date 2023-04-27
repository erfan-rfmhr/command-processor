import zmq
import os


async def server():
    # Define the endpoint for the server
    server_endpoint = os.getenv("SERVER_ENDPOINT", "tcp://*:5555")

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