from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

rooms = {}

@app.get("/")
async def home():
    with open("index1.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())


@app.websocket("/ws/{room}")
async def websocket_endpoint(websocket: WebSocket, room: str):

    await websocket.accept()

    if room not in rooms:
        rooms[room] = []

    rooms[room].append(websocket)

    username = ""

    try:
        while True:

            data = await websocket.receive_json()

            if data["type"] == "join":
                username = data["user"]

            for connection in rooms[room]:
                await connection.send_json(data)

    except WebSocketDisconnect:

        rooms[room].remove(websocket)

        for connection in rooms[room]:
            await connection.send_json({
                "type": "leave",
                "user": username
            })