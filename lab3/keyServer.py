import socket
from socket import *


def runServer():
    myPort = 8000
    host = "127.0.0.1"
    mySocket = socket(AF_INET, SOCK_STREAM)
    mySocket.settimeout(60)
    clientKeys = {}
    try:
        mySocket.bind((host, myPort))
        print("KeyServer listening")
        listening = True
        mySocket.listen()
        while listening:
            connection, _address = mySocket.accept()
            msg = connection.recv(1024).decode()
            if 'SHUTDOWN' == msg.split(" ")[0]:
                print("KeyServer: Got shutdown command")
                listening = False
                connection.send("KeyServer stopping".encode())
            else:
                if 'REGISTER' == msg.split(" ")[0]:
                    registerClient(msg, clientKeys, connection)
                elif 'GET' == msg.split(" ")[0]:
                    returnKey(msg, clientKeys, connection)
                else:
                    print("KeyServer: ERROR, wrong keyword")
                    connection.send("ERROR, wrong keyword".encode())
            connection.close()

    except TimeoutError:
        # print('\t\tTimeout on socket')
        pass

    print("KeyServer stopping")


def registerClient(msg, clientKeys, connection):
    print("KeyServer: Got request to register new client key")
    try:
        _registerCommand, clientId, clientKey = msg.split(" ", 2)  # needs to split the msg 2 times
        if clientId in clientKeys.keys():
            print("KeyServer: Updated key of client with id", clientId, sep=" ")
        else:
            print("KeyServer: Registered client with id", clientId, sep=" ")
        clientKeys[clientId] = clientKey
        connection.send("Registered successfully".encode())
    except ValueError:
        print("KeyServer: ERROR, wrong command format")
        connection.send("ERROR, wrong command format".encode())


def returnKey(msg, clientKeys, connection):
    print("KeyServer: Got request to retreave key")
    try:
        _getCommand, clientId = msg.split(" ")
        if clientId in clientKeys.keys():
            print("KeyServer: Retreaved key of client with id", clientId, sep=" ")
            connection.send(clientKeys[clientId].encode())
        else:
            print("KeyServer: No key found for client with id", clientId, sep=" ")
            resp = "ERROR: no key found for client " + clientId
            connection.send(resp.encode())
    except ValueError:
        print("KeyServer: ERROR, wrong command format")
        connection.send("ERROR, wrong command format".encode())


if __name__ == "__main__":
    runServer()
