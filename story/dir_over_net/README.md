# Directories over the network

A problem with the previous program is that you can only send one file once the
program has started running. If you want to send another file you have to run
the program again after editing it.

Instead what people started doing is modifying the program to send any file
that the person on the other end requested. People would ask for a file path
and the server would check if that path exists and return it.

For example, the program in this folder returns files contained in the `www`
directory. It's still the old program but has been modified slightly to receive
a path and return that file.

```python
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
```

For example to access the INSTALL file we can run the command `echo -e
'www/INSTALL.md\n'|nc localhost 8000` and we will see the contents of the
INSTALL file.
