
from background_runner import BackgroundRunner
from fastapi import FastAPI, WebSocket, Depends, File, HTTPException, status, UploadFile, Form, Response, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import asyncio
import cv2
from db import get_db
import os
from dotenv import load_dotenv
import boto3
from db.models import KnownFace
import uuid
from botocore.exceptions import ClientError
from fastapi.middleware.cors import CORSMiddleware



load_dotenv()

access_key = os.getenv("ACCESS_KEY")
secret_access_key = os.getenv("SECRET_ACCESS_KEY")


s3 = boto3.client(
    "s3",
    region_name="us-east-1", 
    aws_access_key_id = access_key,
    aws_secret_access_key= secret_access_key
)

event_clients = set() 

async def send_event(message: str):
    for websocket in list(event_clients):
        try:
            await websocket.send_json({"message": message, "time" : runner.state.last_time,})
        except WebSocketDisconnect:
            event_clients.discard(websocket)
        except Exception:
            event_clients.discard(websocket)



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/known-faces")
async def add_known_faces(file: UploadFile = File(...), name: str = Form(...), db :AsyncSession =  Depends(get_db)):

    res = await db.execute(select(KnownFace).where(KnownFace.name == name))
    registered_known_face = res.scalar_one_or_none()
    if registered_known_face is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Face already registered")
    id = uuid.uuid4()
    image = file.file
    face = KnownFace(id = id, name = name)

    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None,
        lambda: s3.upload_fileobj(
            image,
            "louisator-known-faces",
             str(id),
             ExtraArgs={"ContentType": file.content_type},
      ))

    await face.save(db)

    return Response(status_code=204)


async def get_known_faces(db: AsyncSession):
    known_names = await db.execute(select(KnownFace))
    results = []

    for face in known_names.scalars().all():
        id = str(face.id)
        try:
            url = await asyncio.get_running_loop().run_in_executor(
                None, lambda: s3.get_object(Bucket="louisator-known-faces", Key = id)["Body"].read()
            )
        except ClientError:
            url = None

        results.append(( face.name,  url))

    return results

runner : BackgroundRunner = None


@app.on_event("startup")
async def app_start():
    global runner
    db_generator = get_db()
    db = await anext(db_generator)

    try:
        known_faces = await get_known_faces(db)
    finally:
        await db_generator.aclose()

    runner = BackgroundRunner(send_event, known_faces)
    asyncio.create_task(runner.activate())

@app.websocket("/camera")
async def camera(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            success, frame = cv2.imencode(".jpg", runner.frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
            if not success:
                continue
            try:

                await asyncio.wait_for(
                    websocket.send_bytes(frame.tobytes()),
                    timeout=1.0
                )
            except asyncio.TimeoutError:
                break

            await asyncio.sleep(0.25)
    except WebSocketDisconnect:
        pass


@app.websocket("/data")
async def data(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.send_json( {
        "speed": runner.state.speed,
        "activity": runner.state.activity,
        "time" : runner.state.last_time,
        "num_obj_detect" : runner.state.num_obj_detected
    })
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        pass


@app.websocket("/events")
async def event(websocket: WebSocket):
    await websocket.accept()
    event_clients.add(websocket)
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect: 
        pass
    finally:
        event_clients.discard(websocket)




