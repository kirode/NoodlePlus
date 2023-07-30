from websockets.sync.client import ClientConnection, connect as ws_connect

from src.models import SelectResponse, Response


class WsConnection:

    def __init__(self, websocket):
        self.ws: ClientConnection = websocket

    def send_model(self, model):
        data = model.model_dump_json(exclude_none=True)
        self.ws.send(data)

    def recv_model(self, model) -> Response | SelectResponse:
        data = self.ws.recv(timeout=10)
        return model.model_validate_json(data)
