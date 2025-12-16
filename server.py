import socket 
import threading 
import queue
import os
import json
# from chatterbot import ChatBot
# from chatterbot.trainers import ChatterBotCorpusTrainer

# chatbot = ChatBot('Ron Obvious')
# trainer = ChatterBotCorpusTrainer(chatbot)
# trainer.train("./chatterbot-corpus-master/chatterbot_corpus/data/english/")


messages = queue.Queue()
clients = []
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("0.0.0.0", 9999))
def receive(): 
    while True: 
        try:
            message, addr = server.recvfrom (1024)
            messages.put((message, addr))
            if("///" in message.decode()):
                if("///true" in message.decode()):
                    server.sendto(f"New member joined!".encode(), addr)
                elif("///new" in message.decode()):
                    credentials = message.decode().split("--")
                    users
                    with open("users.json", "r") as f:
                        users = json.load(f)
                    users[credentials[2]] == credentials[1]
                    with open("users.json", "w") as f:
                        json.dump(users, f)
                    server.sendto(f"New member joined!".encode(), addr)
                    pass
            if addr not in clients:
                if os.path.exists("users.json"):
                    with open("users.json", "r") as f:
                        users = json.load(f)
                        if(message.decode() in users):
                            username = message.decode()
                            password = users[username]
                            server.sendto(f"///authentication--{password}--{username}".encode(), client)
                pass
        except:
            pass


def broadcast():
    print("spinning server")
    while True:
        while not messages.empty():
            message, addr = messages.get()
            if addr not in clients:
                clients.append (addr)
            for client in clients:
                try:
                    if message.decode().startswith("SIGNUP_TAG:"):
                        name = message.decode()[message.decode().index(":")+1:]
                        server.sendto(f"{name} joined!".encode(), client)
                    elif addr[1] == client[1]:
                        pass
                    else:
                        server.sendto(message, client)
                except:
                    clients.remove(client)

t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()


