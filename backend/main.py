
from background_runner import BackgroundRunner
from fastapi import FastAPI, WebSocket
import asyncio
import cv2


runner = BackgroundRunner()
app = FastAPI()



@app.on_event("start_up")
async def app_start():
    asyncio.create_task(runner.activate())

@app.websocket("/camera")
async def camera(websocket: WebSocket):
    await websocket.accept()
    while True:
       frame = cv2.imencode(".png", runner.frame)[1]
       await websocket.send_bytes(frame.tobytes())
       await asyncio.sleep(0.5)
