import socket

def run_client(lb_ip, lb_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((lb_ip, lb_port))
        print(f"[Client] Connected to load balancer at {lb_ip}:{lb_port}")

        # Handle username prompt
        msg = s.recv(1024).decode()
        print(msg, end='')
        username = input()
        s.sendall(username.encode())

        # Handle password prompt
        msg = s.recv(1024).decode()
        print(msg, end='')
        password = input()
        s.sendall(password.encode())

        # Check auth response
        auth_response = s.recv(1024).decode().strip()
        if auth_response == "AUTH_SUCCESS":
            print("[Client] Authentication successful!")
        else:
            print("[Client] Authentication failed. Disconnecting.")
            return

        # Now allow commands
        while True:
            cmd = input("Enter command (GET key / SET key value): ")
            if cmd.lower() in ['exit', 'quit']:
                break
            s.sendall(cmd.encode())
            response = s.recv(1024).decode()
            print(f"[Server Response]: {response}")

if __name__ == "__main__":
    import sys
    lb_ip = sys.argv[1]  # Load balancer IP (192.168.0.106)
    lb_port = int(sys.argv[2])  # Load balancer port (5000)
    run_client(lb_ip, lb_port)
