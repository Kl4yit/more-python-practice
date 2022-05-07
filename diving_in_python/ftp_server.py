import socket

with socket.socket() as sock:
    sock.bind(("", 10001))
    sock.listen()
    
    while True:
        conn, addr = sock.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                if data.decode("utf8").rstrip('\n').split()[-1] == '*':
                    print('in')
                    conn.sendall("ok\npalm.cpu 2.0 1150864247\npalm.cpu 0.5 1150864248\neardrum.cpu 3.0 1150864250\n\n".encode("utf8"))
                print(data.decode("utf8"))