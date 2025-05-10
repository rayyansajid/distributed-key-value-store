import socket
import threading

# List of backend servers (same machine, different ports)
servers = [('192.168.0.106', 5001), ('192.168.0.106', 5002), ('192.168.0.106', 5003)]
server_index = 0
lock = threading.Lock()

def get_next_server():
    global server_index
    with lock:
        srv = servers[server_index]
        server_index = (server_index + 1) % len(servers)
    return srv

def forward(source, destination):
    try:
        while True:
            data = source.recv(1024)
            if not data:
                break
            destination.sendall(data)
    except:
        pass
    finally:
        source.close()
        destination.close()

def handle_client(client_conn, client_addr):
    print(f"[Load Balancer] Client connected: {client_addr}")
    backend_ip, backend_port = get_next_server()
    try:
        backend_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        backend_conn.connect((backend_ip, backend_port))
        print(f"[Load Balancer] Forwarding client {client_addr} to backend {backend_ip}:{backend_port}")

        # Two threads for bidirectional forwarding
        threading.Thread(target=forward, args=(client_conn, backend_conn)).start()
        threading.Thread(target=forward, args=(backend_conn, client_conn)).start()

    except Exception as e:
        print(f"[Load Balancer] Error connecting to backend {backend_ip}:{backend_port} -> {e}")
        client_conn.sendall(b"Backend server error")
        client_conn.close()

def start_balancer(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('192.168.0.106', port))  # SERVER IP
        s.listen()
        print(f"[Load Balancer] Listening on 192.168.0.106:{port}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_balancer(5000)
