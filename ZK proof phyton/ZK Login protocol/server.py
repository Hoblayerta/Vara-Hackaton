import socket
import random
import hashlib

def H(*args) -> int:
    """A one-way hash function."""
    a = ":".join(str(a) for a in args)
    return int(hashlib.sha256(a.encode("utf-8")).hexdigest(), 16)

# Given large prime N
N = """00:c0:37:c3:75:88:b4:32:98:87:e6:1c:2d:a3:32:
       4b:1b:a4:b8:1a:63:f9:74:8f:ed:2d:8a:41:0c:2f:
       c2:1b:12:32:f0:d3:bf:a0:24:27:6c:fd:88:44:81:
       97:aa:e4:86:a6:3b:fc:a7:b8:bf:77:54:df:b3:27:
       c7:20:1f:6f:d1:7f:d7:fd:74:15:8b:d3:1c:e7:72:
       c9:f5:f8:ab:58:45:48:a9:9a:75:9b:5a:2c:05:32:
       16:2b:7b:62:18:e8:f1:42:bc:e2:c3:0d:77:84:68:
       9a:48:3e:09:5e:70:16:18:43:79:13:a8:c3:9c:3d:
       d0:d4:ca:3c:50:0b:88:5f:e3"""

N = int("".join(N.split()).replace(":", ""), 16)
g = 2  # Modulo for our generator
k = H(N, g)
F = '#0x'  # Format specifier

# In-memory storage for users
users = {}

def create_account(u, s, v):
    """Create a new account with a username, salt (s), and verifier (v)."""
    users[u] = {'s': s, 'v': v}  # Store user, s, and v in memory
    print(f"Account created: {u} with s: {s} and v: {v}")

def login(u):
    """Handle login request by checking if the user exists."""
    if u in users:
        s = users[u]['s']
        v = users[u]['v']
        print(f"User {u} found with s: {s} and v: {v}")
        return s, v
    else:
        print(f"User {u} not found!")
        return None, None

def generate_B(u):
    """Generate the server's response B."""
    b = random.randint(0, 255)  # Server-side random value 'b'
    B = (k * users[u]['v'] + pow(g, b, N)) % N  # Compute B = k*v + g^b mod N
    print(f"Server sends B: {B} for user {u} with salt: {users[u]['s']}")
    return B,b

def handle_client(client_socket):
    try:
        # Step 1: Handle CREATE account
        command = client_socket.recv(1024).decode()  # Receive command from client
        if command == "CREATE":
            data = client_socket.recv(1024).decode().split(",")  # Receive account data
            u, s_hex, v_hex = data[0], data[1], data[2]  # Extract account details

            # Convert from hex to integers
            s = int(s_hex, 16)
            v = int(v_hex, 16)

            create_account(u, s, v)  # Create the account in memory
            client_socket.send(f"Account created: {u}".encode())  # Send success message to client

        # Step 2: Handle LOGIN
        command = client_socket.recv(1024).decode()  # Receive command for login
        if command == "LOGIN":
            data = client_socket.recv(1024).decode().split(",")  # Receive login data
            u = data[0]  # Extract username
            A_hex = data[1]  # Extract A (hex)
            A = int(A_hex, 16)  # Convert A from hex to integer

            s, v = login(u)  # Retrieve salt (s) and verifier (v) for the user
            if s is not None:
                # Generate B and send back to the client
                B,b = generate_B(u)
                B_hex = hex(B)[2:]  # Convert B to a hex string, removing the '0x' prefix
                s_hex = hex(s)[2:]  # Convert s to a hex string

                response = f"B:{B_hex}, s:{s_hex}"
                client_socket.send(response.encode())  # Send B and s to client
                
                # Step 3: Wait for session key from client
                session_key = client_socket.recv(1024).decode()
                print(f"Received session key from client: {session_key}")
                
                # Server generates its own session key
                I = H(A_hex, B_hex)  # Scrambling parameter
                S_s = pow(A * pow(v, I, N), b, N)  # Corrected session key calculation
                print("check")
                print(S_s)
                print("check")
                K_s = H(S_s)  # Server's session key

                print(f"Generated server session key: {K_s}")

                # Compare session keys
                if session_key == str(K_s):
                    client_socket.send("Correct login credentials".encode())
                    print("Correct login credentials")
                else:
                    client_socket.send("Incorrect login credentials".encode())
                    print("Incorrect login credentials")
            else:
                client_socket.send("Invalid credentials".encode())  # Invalid login attempt
        else:
            client_socket.send("Invalid command".encode())  # Invalid command

    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)
    print("Server is listening on port 12345...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")
        handle_client(client_socket)

if __name__ == "__main__":
    start_server()
