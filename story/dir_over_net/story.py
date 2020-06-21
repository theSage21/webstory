import socket
import sys

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
addr = ("localhost", 8000)
s.bind(addr)
s.listen(1)


def sendfile(path, sc):
    n = 0
    with open(path, "rb") as fl:
        data = fl.read(1024)
        while data:
            n += len(data)
            sc.send(data)
            data = fl.read(1024)
    print(sc.getpeername(), f"closed after sending {n} bytes")
    sc.close()


while True:
    print("Listening at", addr)
    sc, address = s.accept()
    print(sc.getpeername(), "connected")
    path = sc.recv(1024).decode().strip()
    sendfile(path, sc)
s.close()
