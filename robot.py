import random
import socket
import threading
from openai import OpenAI

clientAPI = OpenAI(api_key="key_here")


def chatAPI(chat):
    print(chat)
    print("Getting chat from GPT")
    response = clientAPI.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": (
                    "Talk to your friends based on conversation. "
                    "Don't mention your name, just the response. "
                    f"Participate in the conversation with max 50 words: {chat}"
                )
            }
        ]
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content


# Replace this with your actual LAN IP or use "" to let OS choose
my_ip = input("Enter server ip you want to connect to: ")
SERVER_IP = my_ip  # <-- replace with your server LAN IP
SERVER_PORT = 9999

# Bind client socket to a random port
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("",random.randint(8000,9000)))
startRobot = True
conversation = []

def receive(): 
    justResponded = False
    while True:
        try:
            message, _ = client.recvfrom(1024)
            conversation.append(message.decode())
            if("/ai" in message.decode()):
                chatAPI(message.decode())
                response = chatAPI(" ".join(conversation))
                client.sendto(f"{response}".encode(), (SERVER_IP, SERVER_PORT))
                
        except Exception as e: 
            print("Error receiving:", e)

# Start receiver thread
t = threading.Thread(target=receive, daemon=True)
t.start()

# Main loop to send messages
while True:
    if startRobot:
        message = input("")
        if message == "!q":
            print("Exiting...")
            break
        else:
            client.sendto("AI JOINED SERVER".encode(), (SERVER_IP, SERVER_PORT))
        startRobot = False
