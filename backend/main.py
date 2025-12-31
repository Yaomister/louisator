
from background_runner import BackgroundRunner
from fastapi import FastAPI, WebSocket
import asyncio
import cv2



event_clients = set() 


async def send_event(message: str):
    for websocket in list(event_clients):
        try:
            await websocket.send_json({"message": message, "time" : runner.state.last_time,})
        except:
            event_clients.remove(websocket)


runner = BackgroundRunner(send_event)
app = FastAPI()

@app.on_event("startup")
async def app_start():
    asyncio.create_task(runner.activate())

@app.websocket("/camera")
async def camera(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            frame = cv2.imencode(".png", runner.frame)[1]
            await websocket.send_bytes(frame.tobytes())
            await asyncio.sleep(0.015)
    except: 
        pass


@app.websocket("/data")
async def data(websocket: WebSocket):
    await websocket.accept(),
    try:
        while True:
            await websocket.send_json( {
        "speed": runner.state.speed,
        "activity": runner.state.activity,
        "time" : runner.state.last_time,
        "num_obj_detect" : runner.state.num_obj_detected
    })
            await asyncio.sleep(5)
    except:
        pass


@app.websocket("/events")
async def event(websocket: WebSocket):
    await websocket.accept()
    event_clients.add(websocket)
    try:
        while True:
            await asyncio.sleep(1)
    except: 
        pass
    finally:
        event_clients.remove(websocket)
