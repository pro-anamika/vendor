from websocket import create_connection
import json
url = 'ws://localhost:8000/ws/chat/kl/' # change to host name on prod server

def send_message_to_socket(message, url=url,):
    ws = create_connection(url)
    ws_msg = json.dumps({"message":message})
    ws.send(ws_msg)
