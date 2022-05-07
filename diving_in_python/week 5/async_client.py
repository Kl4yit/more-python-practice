import asyncio
async def tcp_echo_client(message, loop):
    reader, writer = await asyncio.open_connection('127.0.0.1', 10001)

    print('send: %r' % message)
    writer.write(message.encode())
    writer.close()

loop = asyncio.get_event_loop()
message = 'hello world'
for i in range(100):
    loop.run_until_complete(tcp_echo_client(message, loop))
loop.close()
