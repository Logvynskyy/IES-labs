from fastapi import WebSocket, WebSocketDisconnect, FastAPI
from typing import Set

# FastAPI app setup
app = FastAPI()
# WebSocket subscriptions
subscriptions: Set[WebSocket] = set()

# FastAPI WebSocket endpoint
@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    subscriptions.add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        subscriptions.remove(websocket)


# Function to send data to subscribed users
async def send_data_to_subscribers(data):
    for websocket in subscriptions: 
        await websocket.send_json(json.dumps(data))
