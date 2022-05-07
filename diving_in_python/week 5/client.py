import socket
from operator import itemgetter
import time


class ClientError(OSError):
    """ An error occured while sending data """
    pass


class Client:
    def __init__(self, ip_address, port, timeout=None):
        self.ip_address = ip_address
        self.port = port
        self.timeout = timeout
        self.buffer_size = 1024
        self.sock = socket.create_connection((self.ip_address, self.port), self.timeout)
        # with socket.create_connection((self.ip_address, self.port), self.timeout) as sock:
        #     self.sock = sock

    def get(self, key):
        strin = f"get {key}\n"
        self.sock.sendall(strin.encode("utf8"))
        rdata = self.sock.recv(self.buffer_size)
        data = rdata.decode('utf8').rstrip('\n').split('\n')
        if data[0] != 'ok':
            raise ClientError
            return
        res = {}
        for i in range(1, len(data)):
            item = data[i].split()
            if not item[0] in res.keys():
                res[item[0]] = []
            res[item[0]].append((int(item[2]), float(item[1])))
        for key, val in res.items():
            res[key] = sorted(val, key=itemgetter(0))
        return res

    def put(self, key, value, timestamp=int(time.time())):
        strin = f"put {key} {str(value)} {str(timestamp)}\n"
        try:
            self.sock.sendall(strin.encode("utf8"))
            nice = self.sock.recv(self.buffer_size)
        except OSError:
            raise ClientError


    