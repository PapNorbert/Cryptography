import socket
import sys
import threading
from socket import *
from ast import literal_eval
from knapsack import generate_private_key_knapsack, create_public_key_knapsack, encrypt_mh, decrypt_mh
from solitaire import checkSolitaireKey, generate_half_solitaire_key, generate_second_half_solitaire_key, \
     en_decrypt_solitaire

host = '127.0.0.1'
keyServerPort = 8000


class MyThread(threading.Thread):
    def __init__(self, threadID, clientSocket, myPort, secondPort, privateKey):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.clientSocket = clientSocket
        self.myPort = myPort
        self.otherClientPort = secondPort
        self.otherClientpublicKey = ''
        self.privateKey = privateKey
        self.solitaireKey = ''

    def run(self):
        self.connectToClient()

    def connectToClient(self):
        try:
            # print(f'thread {self.threadID} started\n')

            self.clientSocket.connect((host, self.otherClientPort))
            print('Connected to socket of client with id', self.otherClientPort)
            self.otherClientpublicKey = getOtherClientPublicKey(self.otherClientPort)
            self.establishConnectionInitializer()

            print('Starting conversation using solitaire encryption')

            # TODO : sending receiveing - read text

        except Exception as exception:
            print(exception)

        finally:
            self.clientSocket.close()
        # print(f'thread {self.threadID} stopped\n')

    def establishConnectionInitializer(self):
        print('Establishing connection with client', self.otherClientPort)
        message = 'Hello from ' + self.myPort
        print('Sending:', message)
        self.sendMessageMh(message)

        # agreeing on solitaire key
        decryptedResponse = self.receiveMessageMh()
        print('Generating second half of solitaire key')
        self.solitaireKey = literal_eval(decryptedResponse)
        generate_second_half_solitaire_key(self.solitaireKey)
        solitaireKeyString = '[' + ', '.join(str(x) for x in self.solitaireKey) + ']'
        print('Sending the solitaire key to client', self.otherClientPort, ':', solitaireKeyString)
        self.sendMessageMh(solitaireKeyString)

        decryptedResponse = self.receiveMessageMh()
        if decryptedResponse == 'OK':
            print('Agreed on solitaire key:\n\t', self.solitaireKey)

    def sendMessageMh(self, message):
        print('Encrypting message with the public key of client', self.otherClientPort)
        messageEncoded = encrypt_mh(message, self.otherClientpublicKey)
        print('Sending message encrypted with the public key of client', self.otherClientPort)
        self.clientSocket.send(messageEncoded.encode())

    def receiveMessageMh(self):
        response = literal_eval(self.clientSocket.recv(1024).decode)
        print('Decrypting message with own private key')
        decryptedResponse = decrypt_mh(response, self.privateKey)
        print('Got message', decryptedResponse)
        return decryptedResponse


# run: client.py myPort
def main():
    try:  # 1st paramter - own port number
        myPort = int(sys.argv[1])

        privateKey = generate_private_key_knapsack()
        publicKey = create_public_key_knapsack(privateKey)
        registerToKeyServer(myPort, publicKey)

        thread = -1
        secondPort = -1
        connectToOtherClient = False
        try:  # 2nd parameter
            secondPort = int(sys.argv[2])
            connectToOtherClient = True
        except IndexError:
            pass

        if connectToOtherClient:
            clientSocket = socket(AF_INET, SOCK_STREAM)

            thread = MyThread(1, clientSocket, myPort, secondPort, privateKey)
            thread.start()

        mySocket = socket(AF_INET, SOCK_STREAM)
        mySocket.settimeout(10)
        try:
            mySocket.bind((host, myPort))
            print('Listening on my socket at port ', myPort)
            mySocket.listen()
            connection, _address = mySocket.accept()
            print('Other client connected to my socket')

            # receiveing message - establishing connenction
            encryptedMessage = literal_eval(connection.recv(1024).decode())
            # converting string to list of int with literal_eval
            print('Decrypting message with own private key')
            message = decrypt_mh(encryptedMessage, privateKey)
            print('Got message', message)
            # getting other client port and public key
            otherClientPort = message.split(' ')[2]
            otherClientPublicKey = getOtherClientPublicKey(otherClientPort)

            # agreeing on a solitaire key
            print('Generating first half of solitaire key')
            solitaireKey = generate_half_solitaire_key()
            solitaireKeyString = '[' + ', '.join(str(x) for x in solitaireKey) + ']'
            print('Sending:', solitaireKeyString)
            print('Encrypting response with the public key of client', otherClientPort)
            encryptedSolitaireKey = encrypt_mh(solitaireKeyString, otherClientPublicKey)
            print('Sending message encrypted with the public key of client', otherClientPort)
            connection.send(encryptedSolitaireKey.encode())

            # got the solitaire key
            encryptedMessage = literal_eval(connection.recv(1024).decode())
            # converting string to list of int with literal_eval
            print('Decrypting message with own private key')
            message = decrypt_mh(encryptedMessage, privateKey)
            print('Got message', message)
            solitaireKey = literal_eval(message)
            if checkSolitaireKey(solitaireKey):
                # solitaire key is correct
                print('Agreed on solitaire key:\n\t', solitaireKey)
                print('Sending: OK')
                print('Encrypting response with the public key of client', otherClientPort)
                encryptedResponse = encrypt_mh('OK', otherClientPublicKey)
                print('Sending message encrypted with the public key of client', otherClientPort)
                connection.send(encryptedResponse.encode())

                print('Starting conversation using solitaire encryption')

                # TODO : sending receiveing - read text

            else:
                errorMessage = 'Got wrong solitaire key, connection could not be established with client ' \
                               + otherClientPort
                print(errorMessage)
                print('Sending:', errorMessage)
                print('Encrypting response with the public key of client', otherClientPort)
                encryptedResponse = encrypt_mh(errorMessage, otherClientPublicKey)
                print('Sending message encrypted with the public key of client', otherClientPort)
                connection.send(encryptedResponse.encode())

            mySocket.close()

        except TimeoutError:
            # print('\t\tTimeout on own socket')
            pass

        if connectToOtherClient:
            thread.join()

    except IndexError:
        print('Please specifie own port number')
    except ValueError:
        print('First parameter must be a number, own port number')


def registerToKeyServer(myPort, myKey):
    keyServerSocket = socket(AF_INET, SOCK_STREAM)
    keyServerSocket.connect((host, keyServerPort))
    print('Registering to keyServer')
    message = 'REGISTER ' + myPort + ' ' + myKey
    keyServerSocket.send(message.encode())
    response = keyServerSocket.recv(1024).decode()
    print('Got response:', response)


def getOtherClientPublicKey(otherClientPort):
    keyServerSocket = socket(AF_INET, SOCK_STREAM)
    keyServerSocket.connect((host, keyServerPort))
    request = 'GET ' + otherClientPort
    print('Requesting the public key of client', otherClientPort)
    keyServerSocket.send(request.encode())
    otherClientpublicKey = keyServerSocket.recv(1024).decode()
    keyServerSocket.close()
    return otherClientpublicKey


if __name__ == "__main__":
    main()
