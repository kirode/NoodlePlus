from websockets.sync.client import ClientConnection, connect


def ws() -> ClientConnection:
    with connect('ws:127.0.0.1:4000') as websocket:
        yield websocket
