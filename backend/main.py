
from background_runner import BackgroundRunner
from fastapi import FastAPI
import asyncio


runner = BackgroundRunner()
app = FastAPI()



@app.on_event("start_up")
async def app_start():
    asyncio.create_task(runner.activate())