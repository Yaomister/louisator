import asyncio
import math
import cv2
from ultralytics import YOLO
from dataclasses import dataclass


@dataclass
class State:
    moving: bool

class BackgroundRunner:

    def __init__(self):
        self.model = YOLO("model.pt")
        self.video = cv2.VideoCapture.open(0)
        _, self.frame = self.video.read()

    async def activate(self):
        while(True):
            await asyncio.sleep(0.5)
            _frame = self.video.read()[1]
            results = self.model.track(_frame, persist=True, conf = 0.1)
            self.frame = results[0].plot()



