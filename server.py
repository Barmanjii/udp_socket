import socket

# Define the IP address and port to bind the socket
UDP_IP = "0.0.0.0"  # localhost
UDP_PORT = 12345       # Arbitrary port number

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the IP address and port
sock.bind((UDP_IP, UDP_PORT))

print("UDP server is running...")

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)


while True:
    # Receive data from the client
    data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes

    if data.decode().upper() == "IP":
        print("Request for IP received")
        sock.sendto(ip_address.encode(), addr)

# Close the socket
sock.close()
