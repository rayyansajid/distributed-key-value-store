import socket

class KeyValueStore:
    def __init__(self):
        # Each client has its own key-value store
        self.stores = {}

    def authenticate(self, client_id):
        """Authenticate a client and create a store if it doesn't exist."""
        if client_id not in self.stores:
            self.stores[client_id] = {}
        return client_id

    def put(self, client_id, key, value):
        """Store a key-value pair for the authenticated client."""
        if client_id not in self.stores:
            return "Client not authenticated"
        self.stores[client_id][key] = value
        return f"Stored: {key} -> {value}"

    def get(self, client_id, key):
        """Retrieve a value for the authenticated client."""
        if client_id not in self.stores:
            return "Client not authenticated"
        return self.stores[client_id].get(key, "Key not found")

def start_server(host='127.0.0.1', port=65432):
    kv_store = KeyValueStore()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Server listening on {host}:{port}")

        while True:
            client_socket, client_address = server_socket.accept()
            with client_socket:
                print(f"Connected by {client_address}")
                authenticated_client = None  # Track the authenticated client

                while True:
                    data = client_socket.recv(1024).decode('utf-8')
                    if not data:
                        break

                    parts = data.split()
                    if len(parts) < 2:
                        response = "Invalid command"
                    else:
                        command, *args = parts

                        if command == "AUTH":
                            # Authenticate the client
                            if len(args) != 1:
                                response = "Invalid AUTH command"
                            else:
                                client_id = args[0]
                                authenticated_client = kv_store.authenticate(client_id)
                                response = f"Authenticated as {client_id}"
                        elif authenticated_client:
                            if command == "PUT" and len(args) == 2:
                                key, value = args
                                response = kv_store.put(authenticated_client, key, value)
                            elif command == "GET" and len(args) == 1:
                                key = args[0]
                                response = kv_store.get(authenticated_client, key)
                            else:
                                response = "Invalid command"
                        else:
                            response = "Not authenticated"

                    client_socket.sendall(response.encode('utf-8'))

if __name__ == "__main__":
    start_server()