import asyncio
#
# {
#   'palm.cpu': [
#     (1150864247, 0.5),
#     (1150864248, 0.5)
#   ]
# }


class ClientServerProtocol(asyncio.Protocol):
    storage = {}

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = self.process_data(data.decode('utf8'))
        resp = f'{resp[0]}{resp[1]}\n\n'
        self.transport.write(resp.encode('utf8'))


    def process_data(self, data):
        data = data.rstrip('\n').split()
        if len(data) < 5 and data[0] == 'put':
            if not data[1] in ClientServerProtocol.storage.keys():
                ClientServerProtocol.storage[data[1]] = []
            # is_metric = (data[3], data[2]) in ClientServerProtocol.storage[data[1]]
            is_metric = data[3] in [item[0] for item in ClientServerProtocol.storage[data[1]]]
            ClientServerProtocol.storage[data[1]] += [(data[3], data[2])] if not is_metric else []
            return ['ok', '']
        if len(data) > 2 or data[0] != 'get':
            return ['error', '\nwrong command']
        res = ''
        if (not data[1] in ClientServerProtocol.storage.keys()) and data[1] != '*':
            return ['ok', res]
        keys = ClientServerProtocol.storage.keys() if data[1] == '*' else [data[1]]
        for key in keys:

            for item in ClientServerProtocol.storage[key]:
                res += '\n' + ' '.join([key, item[1], item[0]])
        return ['ok', res]


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
