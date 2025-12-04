import socket 
import threading 
import queue
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot('Ron Obvious')
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("./chatterbot-corpus-master/chatterbot_corpus/data/english/")


messages = queue.Queue()
clients = []
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("0.0.0.0", 9999))
def receive(): 
    while True: 
        try:
            message, addr = server.recvfrom (1024)
            messages.put((message, addr))
        except:
            pass


def broadcast():
    while True:
        while not messages.empty():
            message, addr = messages.get ()
            print (message. decode())
            if addr not in clients:
                clients. append (addr)
            for client in clients:
                try:
                    if message.decode().startswith("SIGNUP_TAG:"):
                        name = message.decode()[message.decode().index(":")+1:]
                        server.sendto(f"{name} joined!", client)
                    else:
                        server.sendto(message)
                except:
                    clients.remove

t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()


# chatBot
while True:
    message = input("Enter message:")

    respose = chatbot.get_response(f"{message}")
    print(respose)

