import socket

class KeyValueStore:
    def __init__(self):
        self.store = {}

    def put(self, key, value):
        self.store[key] = value
        return f"Stored: {key} -> {value}"

    def get(self, key):
        return self.store.get(key, "Key not found")

def start_server(host='127.0.0.1', port=65432):
    # Initialize the key-value store
    kv_store = KeyValueStore()

    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Server listening on {host}:{port}")

        while True:
            # Wait for a connection
            client_socket, client_address = server_socket.accept()
            with client_socket:
                print(f"Connected by {client_address}")
                while True:
                    # Receive data from the client
                    data = client_socket.recv(1024).decode('utf-8')
                    if not data:
                        break

                    # Parse the command
                    parts = data.split()
                    if len(parts) < 2:
                        response = "Invalid command"
                    else:
                        command, key = parts[0], parts[1]
                        if command == "PUT" and len(parts) == 3:
                            value = parts[2]
                            response = kv_store.put(key, value)
                        elif command == "GET":
                            response = kv_store.get(key)
                        else:
                            response = "Invalid command"

                    # Send the response back to the client
                    client_socket.sendall(response.encode('utf-8'))

if __name__ == "__main__":
    start_server()