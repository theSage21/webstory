# Getting files from a network

It all started when people wanted to transfer files which were on another computer to their own system.

To do this you needed two computers. One which has the file and will serve it
and another which is requesting access.

The way that the access is requested and provided is over sockets. For the
purposes of this story it suffices to say that sockets are like telephones.
Every computer has a "phone number". Most look like "127.0.0.1:8000".

Now, to request access over a network we can use the `nc` program on ubuntu.
For example to establish a connection with `127.0.0.1:8000` we can issue a
command like `nc 127.0.0.1 8000` and the link is established. Of course someone
has to be listening on the other side.

For the listening part, we write a python program.

```python
import socket
import sys

# Establish a listening address
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
addr = ("localhost", 8000)
s.bind(addr)
s.listen(1)

# Start listening
while True:
    print("Listening at", addr)
    sc, address = s.accept()
    print(sc.getpeername(), "connected")
    # Transfer the file
    n = 0
    with open("README.md", "rb") as fl:
        data = fl.read(1024)
        while data:
            n += len(data)
            sc.send(data)
            data = fl.read(1024)
    print(sc.getpeername(), f"closed after sending {n} bytes")
    sc.close()
s.close()
```

The program above sends this README file to whoever connects to it. Take your
time and go through this program. Programs like these are called servers.


If there are any questions, [open an issue](https://github.com/theSage21/webstory/issues/new) on this repo.
