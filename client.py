import random
import socket
import threading

# Replace this with your actual LAN IP or use "" to let OS choose

SERVER_IP = "172.17.215.200"  # <-- replace with your server LAN IP
SERVER_PORT = 9999

# Bind client socket to a random port
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind((SERVER_IP,random.randint(8000,9000)))


name = input("Nickname: ")

def receive(): 
    print("Starting receiver")
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print(message.decode())
        except Exception as e: 
            print("Error receiving:", e)

# Start receiver thread
t = threading.Thread(target=receive, daemon=True)
t.start()

# Send signup message
client.sendto(f"SIGNUP_TAG:{name}".encode(), (SERVER_IP, SERVER_PORT))

# Main loop to send messages
while True:
    message = input("")
    if message == "!q":
        print("Exiting...")
        break
    else:
        client.sendto(f"{name}: {message}".encode(), (SERVER_IP, SERVER_PORT))
