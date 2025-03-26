import socket

def send_request(command):
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(('127.0.0.1', 65432))
        client_socket.sendall(command.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Response: {response}")

if __name__ == "__main__":
    while True:
        print("Enter command (e.g., 'PUT key value' or 'GET key'):")
        user_input = input()
        if user_input.lower() == "exit":
            break
        send_request(user_input)
            