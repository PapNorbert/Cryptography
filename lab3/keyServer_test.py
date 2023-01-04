import socket
import threading
import time
from socket import *
import pytest

from keyServer import runServer

keyServerPort = 8000
host = "127.0.0.1"
server_thread = threading.Thread(target=runServer)


# start keyServer before tests
@pytest.fixture(scope="session", autouse=True)
def start_server(request):
    server_thread.start()
    time.sleep(0.1)
    request.addfinalizer(join_thread_finalizer)


def join_thread_finalizer():
    time.sleep(0.1)
    server_thread.join()


def test_keyServer_register_error_no_key():
    testSocket = socket(AF_INET, SOCK_STREAM)
    testSocket.connect((host, keyServerPort))
    testSocket.send('REGISTER 8001'.encode())
    resp = testSocket.recv(1024).decode()
    assert resp == "ERROR, wrong command format"


def test_keyServer_register_ok():
    testSocket = socket(AF_INET, SOCK_STREAM)
    testSocket.connect((host, keyServerPort))
    testSocket.send('REGISTER 8001 [10, 12, 40, 96, 212, 710, 2104, 5534]'.encode())
    resp = testSocket.recv(1024).decode()
    assert resp == "Registered successfully"


def test_keyServer_error_wrong_keyword():
    testSocket = socket(AF_INET, SOCK_STREAM)
    testSocket.connect((host, keyServerPort))
    testSocket.send('REGISTERR 8001 55'.encode())
    resp = testSocket.recv(1024).decode()
    assert resp == "ERROR, wrong keyword"


def test_keyServer_error_wrong_keyword2():
    testSocket = socket(AF_INET, SOCK_STREAM)
    testSocket.connect((host, keyServerPort))
    testSocket.send('GETt 8001'.encode())
    resp = testSocket.recv(1024).decode()
    assert resp == "ERROR, wrong keyword"


def test_keyServer_get_ok():
    testSocket = socket(AF_INET, SOCK_STREAM)
    testSocket.connect((host, keyServerPort))
    testSocket.send('GET 8001'.encode())
    resp = testSocket.recv(1024).decode()
    assert resp == "[10, 12, 40, 96, 212, 710, 2104, 5534]"


def test_keyServer_get_error_no_id():
    testSocket = socket(AF_INET, SOCK_STREAM)
    testSocket.connect((host, keyServerPort))
    testSocket.send('GET'.encode())
    resp = testSocket.recv(1024).decode()
    assert resp == "ERROR, wrong command format"


def test_keyServer_get_error_no_key_found_for_id():
    testSocket = socket(AF_INET, SOCK_STREAM)
    testSocket.connect((host, keyServerPort))
    testSocket.send('GET 8002'.encode())
    resp = testSocket.recv(1024).decode()
    assert resp == "ERROR: no key found for client 8002"


def test_keyServer_shutdown():
    testSocket = socket(AF_INET, SOCK_STREAM)
    testSocket.connect((host, keyServerPort))
    testSocket.send('SHUTDOWN'.encode())
    resp = testSocket.recv(1024).decode()
    assert resp == "KeyServer stopping"
