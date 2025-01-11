import socket
import random
import hashlib

def H(*args) -> int:
    """A one-way hash function."""
    a = ":".join(str(a) for a in args)
    return int(hashlib.sha256(a.encode("utf-8")).hexdigest(), 16)

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

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))
print("Connected to the server.")

def create_account():
    """Create a new account on the server."""
    print("Creating a new account...")
    u = input("Enter your username: ")
    p = input("Enter your password: ")
    s = random.randint(0, 255)
    x = H(s, u, p)  # Hashing the password and other parameters
    v = pow(g, x, N)  # v = g^x mod N

    # Convert v and s to hex
    s_hex = hex(s)[2:]
    v_hex = hex(v)[2:]

    account_data = f"{u},{s_hex},{v_hex}"
    client_socket.send("CREATE".encode())
    client_socket.send(account_data.encode())  # Send account info to the server

    response = client_socket.recv(1024).decode()  # Receive server response
    print(f"Server: {response}")

def login():
    """Login to an existing account."""
    print("Logging into your account...")
    u = input("Enter your username: ")
    p = input("Enter your password: ")
    a = random.randint(0, 255)
    A = pow(g, a, N)  # A = g^a mod N

    A_hex = hex(A)[2:]  # Convert A to a hex string without '0x'

    login_data = f"{u},{A_hex}"
    client_socket.send("LOGIN".encode())
    client_socket.send(login_data.encode())  # Send login info to the server

    response = client_socket.recv(1024).decode()  # Receive server's B and s
    print(f"Server: {response}")
    
    # Step 3: Extract server's B and s, and calculate session key
    response_data = response.split(",")
    B_hex = response_data[0].split(":")[1].strip()
    s_hex = response_data[1].split(":")[1].strip()

    # Convert from hex to integers
    B = int(B_hex, 16)
    s = int(s_hex, 16)

    # Step 4: Calculate the session key on the client side
    I = H(A_hex, B_hex)  # Scrambling parameter
    x = H(s, u, p)  # Client-side session computation
    S_c = pow(B - k * pow(g, x, N), a + I * x, N)  # Corrected session calculation
    print("check")
    print(S_c)
    print("check")
    K_c = H(S_c)  # Client's session key

    print(f"Client's calculated session key: {K_c}")

    # Send session key to the server for verification
    client_socket.send(str(K_c).encode())

    # Step 5: Receive server's verification response
    verification_response = client_socket.recv(1024).decode()
    print(f"Server: {verification_response}")

def main():
    """Prompt the user to choose login or account creation."""
    while True:
        print("Welcome! Choose an option:")
        print("1. Create a new account")
        print("2. Login to your account")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            create_account()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the main function
if __name__ == "__main__":
    main()
