import socket

def send_request(client_socket, command):
    # Send the command to the server
    client_socket.sendall(command.encode('utf-8'))
    # Receive and return the response from the server
    response = client_socket.recv(1024).decode('utf-8')
    return response

def start_client(host='127.0.0.1', port=65432):
    authenticated = False  # Track whether the client is authenticated
    client_id = None       # Store the authenticated client ID

    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        while True:
            if not authenticated:
                print("You must authenticate first using 'AUTH <client_id>'")
            user_input = input("Enter command (e.g., 'AUTH <client_id>', 'PUT key value', or 'GET key'):\n")
            if user_input.lower() == "exit":
                print("Exiting...")
                break

            # Send the command to the server
            response = send_request(client_socket, user_input)

            # Check if authentication was successful
            if user_input.startswith("AUTH"):
                if response.startswith("Authenticated as"):
                    authenticated = True
                    client_id = user_input.split()[1]
                    print(f"You are now authenticated as {client_id}")
                else:
                    print("Authentication failed:", response)
            else:
                if not authenticated:
                    print("You must authenticate first.")
                else:
                    print(f"Response: {response}")

if __name__ == "__main__":
    start_client()