import asyncio
import time
import cv2
from ultralytics import YOLO
from dataclasses import dataclass
import numpy as np


@dataclass
class State:
    last_time: float | None = None
    prev_grey: np.ndarray | None = None
    speed: float = 0.0
    activity: str = "idle"
    seen: set[str] = None
    num_obj_detected = 0

class BackgroundRunner:

    def __init__(self, send_event):
        self.model = YOLO("best.pt")
        self.video = cv2.VideoCapture(0)
        self.state = State()
        _, self.frame = self.video.read()
        self.state.seen = set()
        self.send_event = send_event

    async def activate(self):
        while(True):
            await asyncio.sleep(0.015)
            _frame = self.video.read()[1]
            results = self.model.track(_frame, persist=True, conf = 0.1)
            self.frame = results[0].plot()
            
            grey = cv2.cvtColor(_frame, cv2.COLOR_BGR2GRAY)
            grey = cv2.GaussianBlur(grey, (21, 21), 0)

            now = time.time()


            if (self.state.prev_grey is None):
                self.state.prev_grey = grey
                self.state.last_time = now
                continue
            
            diff = cv2.absdiff(self.state.prev_grey, grey)
            motion = np.mean(diff)

            dt = now - self.state.last_time
            self.state.speed = motion/(max(dt, 0.001))

            self.state.prev_grey = grey

            self.state.last_time = now

            current_id = set()

            for box in results[0].boxes:
                if (box.id is None): 
                    continue
                current_id.add(int(box.id.item()))

            self.state.num_obj_detected = len(current_id)


            not_seen_ids = current_id - self.state.seen

            

            if (len(not_seen_ids) > 0):
                for id in not_seen_ids:
                    for box in results[0].boxes:
                        if (box.id == id):
                            cls_id = int(box.cls)
                            label = results[0].names.get(cls_id, "unknown animal")
                            await self.send_event(f"met a {label.split("-")[1]} 🐾")
                    
            
            self.state.seen = current_id







