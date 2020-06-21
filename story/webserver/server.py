import socket
import sys
from threading import Thread
from queue import Queue

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
addr = ("localhost", 8000)
s.bind(addr)
s.listen(1)
requestQ = Queue()


def get_file(path, sc):
    n = 0
    with open(path, "rb") as fl:
        data = fl.read(1024)
        while data:
            n += len(data)
            sc.send(data)
            data = fl.read(1024)
    print(sc.getpeername(), f"closed after sending {n} bytes")


def put_file(path, sc):
    n = 0
    with open(path, "wb") as fl:
        data = sc.recv(1024)
        while data:
            fl.write(data)
            n += len(data)
            data = sc.recv(1024)
    print(sc.getpeername(), f"closed after receiving {n} bytes")


def handle_request(sock):
    data = sock.recv(1024).decode()
    while "\n" not in data:
        data += sock.recv(1024).decode()
    try:
        instruction, *_ = data.split("\n")
        method, path = instruction.strip().split()
        print(sock.getpeername(), method, path)
        if method.lower() == "get":
            get_file(path, sock)
        elif method.lower() == "put":
            put_file(path, sock)
        else:
            print("Unknown instruction received: ", instruction)
    except Exception as e:
        sock.send(f"Something went wrong: {e}".encode())
    finally:
        sock.close()


def worker():
    global requestQ
    while True:
        sock = requestQ.get()
        handle_request(sock)


n_workers = 1
workers = [Thread(target=worker) for _ in range(n_workers)]
for w in workers:
    w.start()
while True:
    print("Listening at", addr)
    sc, address = s.accept()
    requestQ.put(sc)
s.close()
