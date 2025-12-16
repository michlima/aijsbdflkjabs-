import random
import socket
import threading
import sys
import select
import join


def flush_input():
    while select.select([sys.stdin], [], [], 0)[0]:
        sys.stdin.read(1)

# Replace this with your actual LAN IP or use "" to let OS choose

my_ip = input("Enter server ip you want to connect to: ")
server_ip = my_ip  # <-- replace with your server LAN IP
SERVER_PORT = 9999

# Bind client socket to a random port
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("",random.randint(8000,9000)))


name = input("Nickname: ")

def receive(): 
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print("", end="\r")
            print(f"{message.decode()} \n{name}: ", flush=True)
            sys.stdout.write("\033[1A")  # Move cursor up 1 line
            sys.stdout.write(f"\033[{len(name) + 1}C")
            sys.stdout.flush()
        except Exception as e: 
            print("Error receiving:", e)

# Start receiver thread
t = threading.Thread(target=receive, daemon=True)
t.start()

# Send signup message
client.sendto(f"SIGNUP_TAG:{name}".encode(), (server_ip, SERVER_PORT))

# Main loop to send messages
while True:
    flush_input()
    message = input(f"{name}: ")
    flush_input()
    if message == "!q":
        print("Exiting...")
        print(f"",end="\r")
        client.sendto(f"{name} left the chat!".encode(), (server_ip, SERVER_PORT))
        print("exiting chat...")
        break
    if "/ping" in message:
        try:
            ip = message.split(" ")[1]
            join.ping(ip)
        except Exception as e:
            print(e)
            print("command should be:\n/ping-<place pinging>")
    if "/join" in message:
        newIp =message.split(" ")[1]
        server_ip = newIp
        print(f"joining server {newIp}")
        client.sendto(f"{name} JOINED THE SERVER".encode(), (server_ip, SERVER_PORT))
    else:
        client.sendto(f"{name}: {message}".encode(), (server_ip, SERVER_PORT))
