import socket
import threading

# List of server addresses
SERVERS = [('127.0.0.1', 65432), ('127.0.0.1', 65433), ('127.0.0.1', 65434)]
current_server_index = 0

def handle_client(client_socket):
    global current_server_index

    # Select a server using round-robin
    server_address = SERVERS[current_server_index]
    current_server_index = (current_server_index + 1) % len(SERVERS)

    # Connect to the selected server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect(server_address)

    def forward_data(source, destination):
        while True:
            data = source.recv(1024)
            if not data:
                break
            destination.sendall(data)
        source.close()
        destination.close()

    # Forward data between client and server
    threading.Thread(target=forward_data, args=(client_socket, server_socket)).start()
    threading.Thread(target=forward_data, args=(server_socket, client_socket)).start()

def start_load_balancer(host='127.0.0.1', port=5000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as lb_socket:
        lb_socket.bind((host, port))
        lb_socket.listen()
        print(f"Load balancer listening on {host}:{port}")

        while True:
            client_socket, client_address = lb_socket.accept()
            print(f"New connection from {client_address}")
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()

if __name__ == "__main__":
    start_load_balancer()