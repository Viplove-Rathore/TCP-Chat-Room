import socket
import threading


host = '127.0.0.1' #local host
port = 4545

#create and bind
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    while True:
        try:
            msg = message = client.recv(1024)
            if msg.decode('UTF-8').startswith('KICK'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_kick = msg.decode('UTF-8').split(' ')[1]
                    kick_name(name_to_kick)
                else:
                    client.send('Commend was refused'.encode('UTF-8'))

            elif msg.decode('UTF-8').startswith('BAN'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_ban = msg.decode('UTF-8').split(' ')[1]
                    kick_name(name_to_ban)
                    with open('bans.txt', 'a') as f:
                        f.write(name_to_ban + '\n')
                    print(f'{name_to_ban} has been banned')
                else:
                    client.send('Commend was refused'.encode('UTF-8'))
            else:
                broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} has left the chat!'.encode('UTF-8'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client , address = server.accept()
        print(f'{address} has connected.')

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')

        with open('bans.txt', 'r') as f:
            bans = f.readline()

        if nickname+'\n' in bans:
            client.send('BAN'.encode('UTF-8'))
            client.close()
            continue

        if nickname == 'admin' :
            client.send('PASS'.encode('UTF-8'))
            password = client.recv(1024).decode('UTF-8')

            if password != 'adminpass':
                client.send("REFUSE".encode('UTF-8'))
                client.close()
                continue

        nicknames.append(nickname)
        clients.append(client)

        print(f'{nickname} has joined the chat!'.encode('ascii'))
        broadcast(f'{nickname} has joined the chat!'.encode('ascii'))
        client.send('WELCOME'.encode('ascii'))

        thread = threading.Thread(target = handle_client , args = (client,))
        thread.start()

def kick_name(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send('You were kicked by admin'.encode('UTF-8'))
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(f"{name} has been kicked!".encode('UTF-8'))

print("Server starting...")
receive()
