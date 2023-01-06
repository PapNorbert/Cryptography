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

            sending = True
            while sending:
                text = input('Text to send:\n\t')
                print('Sending text: ', text)
                self.solitaireKey = sendMessageSolitaire(self.clientSocket, text, self.solitaireKey)
                if text.lower() == 'exit':
                    sending = False
                    print('Stopping communication')
                else:
                    decryptedResp, self.solitaireKey = receiveMessageSoltaire(self.clientSocket, self.solitaireKey)
                    if decryptedResp.lower() == 'exit':
                        sending = False
                        print('Stopping communication')
        except Exception as exception:
            print(exception)

        finally:
            self.clientSocket.close()
        # print(f'thread {self.threadID} stopped\n')

    def establishConnectionInitializer(self):
        print('Establishing connection with client', self.otherClientPort)
        message = 'Hello from ' + str(self.myPort)
        print('Sending:', message)
        sendMessageMh(self.clientSocket, message, self.otherClientPort, self.otherClientpublicKey)

        # agreeing on solitaire key
        decryptedResponse = receiveMessageMh(self.clientSocket, self.privateKey)
        print('Generating second half of solitaire key')
        self.solitaireKey = literal_eval(decryptedResponse)
        generate_second_half_solitaire_key(self.solitaireKey)
        solitaireKeyString = '[' + ', '.join(str(x) for x in self.solitaireKey) + ']'
        print('Sending the solitaire key to client', self.otherClientPort, ':', solitaireKeyString)
        sendMessageMh(self.clientSocket, solitaireKeyString, self.otherClientPort, self.otherClientpublicKey)

        decryptedResponse = receiveMessageMh(self.clientSocket, self.privateKey)
        if decryptedResponse == 'OK':
            print('Agreed on solitaire key:\n\t', self.solitaireKey)


# run: client.py myPort
def main():
    try:  # 1st paramter - own port number
        myPort = int(sys.argv[1])
        print('Client with id', myPort, 'started')
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
        mySocket.settimeout(20)
        try:
            mySocket.bind((host, myPort))
            print('Listening on my socket at port ', myPort)
            mySocket.listen()
            connection, _address = mySocket.accept()
            print('Other client connected to my socket')

            # receiveing message - establishing connenction
            message = receiveMessageMh(connection, privateKey)
            # getting other client port and public key
            otherClientPort = message.split(' ')[2]
            otherClientPublicKey = getOtherClientPublicKey(otherClientPort)

            # agreeing on a solitaire key
            print('Generating first half of solitaire key')
            solitaireKey = generate_half_solitaire_key()
            solitaireKeyString = '[' + ', '.join(str(x) for x in solitaireKey) + ']'
            print('Sending:', solitaireKeyString)
            sendMessageMh(connection, solitaireKeyString, otherClientPort, otherClientPublicKey)

            # got the solitaire key
            solitaireKey = literal_eval(receiveMessageMh(connection, privateKey))
            if checkSolitaireKey(solitaireKey):
                # solitaire key is correct
                print('Agreed on solitaire key:\n\t', solitaireKey)
                print('Sending: OK')
                sendMessageMh(connection, 'OK', otherClientPort, otherClientPublicKey)

                print('Starting conversation using solitaire encryption')

                exiting = False
                while not exiting:
                    decryptedMsg, solitaireKey = receiveMessageSoltaire(connection, solitaireKey)
                    if decryptedMsg.lower() == 'exit':
                        exiting = True
                        print('Stopping communication')
                    else:
                        text = input('Answer:\n\t')
                        print('Sending text: ', text)
                        solitaireKey = sendMessageSolitaire(connection, text, solitaireKey)
                        if text.lower() == 'exit':
                            exiting = True
                            print('Stopping communication')

            else:
                errorMessage = 'Got wrong solitaire key, connection could not be established with client ' \
                               + str(otherClientPort)
                print(errorMessage)
                print('Sending:', errorMessage)
                sendMessageMh(connection, errorMessage, otherClientPort, otherClientPublicKey)

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
    print('Registering to keyServer with key', myKey)
    myKeyString = '[' + ', '.join(str(x) for x in myKey) + ']'
    message = 'REGISTER ' + str(myPort) + ' ' + myKeyString
    keyServerSocket.send(message.encode())
    response = keyServerSocket.recv(1024).decode()
    print('Got response:', response)


def getOtherClientPublicKey(otherClientPort):
    keyServerSocket = socket(AF_INET, SOCK_STREAM)
    keyServerSocket.connect((host, keyServerPort))
    request = 'GET ' + str(otherClientPort)
    print('Requesting the public key of client', otherClientPort)
    keyServerSocket.send(request.encode())
    otherClientpublicKey = keyServerSocket.recv(1024).decode()
    keyServerSocket.close()
    return literal_eval(otherClientpublicKey)


def sendMessageMh(clientSocket, message, otherClientPort, otherClientpublicKey):
    print('Encrypting message with the public key of client', otherClientPort)
    messageEncoded = encrypt_mh(message, otherClientpublicKey)
    # converting list of int to string
    messageEncodedString = '[' + ', '.join(str(x) for x in messageEncoded) + ']'
    print('Sending message encrypted with the public key of client', otherClientPort)
    clientSocket.send(messageEncodedString.encode())


def receiveMessageMh(clientSocket, privateKey):
    # converting string to list of int with literal_eval
    response = literal_eval(clientSocket.recv(10240).decode())
    print('Decrypting message with own private key')
    decryptedResponse = decrypt_mh(response, privateKey)
    print('Got message', decryptedResponse)
    return decryptedResponse


def sendMessageSolitaire(clientSocket, message, solitaireKey):
    print('Encrypting message with solitaire key')
    messageEncoded, solitaireKey = en_decrypt_solitaire(message, solitaireKey)
    print('Sending message encrypted with with solitaire key')
    clientSocket.send(messageEncoded.encode())
    return solitaireKey


def receiveMessageSoltaire(clientSocket, solitaireKey):
    response = clientSocket.recv(10240).decode()
    print('Decrypting message with with solitaire key')
    decryptedResponse, solitaireKey = en_decrypt_solitaire(response, solitaireKey)
    print('Got message', decryptedResponse)
    return decryptedResponse, solitaireKey


if __name__ == "__main__":
    main()
