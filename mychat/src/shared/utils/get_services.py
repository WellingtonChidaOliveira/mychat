

class Utils:
    def get_header(websocket, header_name):
        return next((v for k, v in websocket.headers.items() if k.lower() == header_name), None)