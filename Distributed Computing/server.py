import socket
import threading

# Hardcoded user database
users = {
    "alice": "password123",
    "bob": "secret456",
}

store = {}  # Simple key-value store

def authenticate(conn):
    conn.sendall(b"Username: ")
    username = conn.recv(1024).decode().strip()
    conn.sendall(b"Password: ")
    password = conn.recv(1024).decode().strip()
    
    if username in users and users[username] == password:
        conn.sendall(b"AUTH_SUCCESS\n")
        print(f"[Server] {username} authenticated successfully")
        return True
    else:
        conn.sendall(b"AUTH_FAILED\n")
        print(f"[Server] Authentication failed for user '{username}'")
        return False

def handle_client(conn, addr):
    print(f"[Server] Connected by {addr}")
    with conn:
        if not authenticate(conn):
            conn.close()
            return
        
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            parts = data.strip().split()
            if len(parts) == 0:
                continue
            cmd = parts[0].upper()

            if cmd == "GET" and len(parts) == 2:
                key = parts[1]
                value = store.get(key, "Key not found")
                conn.sendall(str(value).encode())

            elif cmd == "SET" and len(parts) >= 3:
                key = parts[1]
                value = ' '.join(parts[2:])
                store[key] = value
                conn.sendall(b"OK")

            else:
                conn.sendall(b"Invalid Command")

def start_server(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('192.168.0.106', port))  # SERVER IP
        s.listen()
        print(f"[Server] Listening on 192.168.0.106:{port}")
        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1])
    start_server(port)
