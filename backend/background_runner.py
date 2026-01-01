import asyncio
import time
import cv2
from ultralytics import YOLO
from dataclasses import dataclass
import numpy as np
from face_detection import FaceDetection


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
        self.facial_recognition = FaceDetection(None)


    async def activate(self):
        while(True):
            await asyncio.sleep(0.25)
            _frame = self.video.read()[1]
            results = self.model.track(_frame, persist=True, conf = 0.1)

            recognized_people = self.facial_recognition.recognize(_frame)

            current_seen = set()

            for name, (top, right, bottom, left) in recognized_people:
                current_seen.add(name)
                cv2.rectangle(_frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(_frame, (left, bottom - 35), (right, top), (0, 0, 255))
                font = cv2.FONT_HERSHEY_COMPLEX
                cv2.putText(_frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

                
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

            for box in results[0].boxes:
                if (box.id is None): 
                    continue
                current_seen.add(int(box.id.item()))

            self.state.num_obj_detected = len(current_seen)


            newly_seen = current_seen - self.state.seen

        
            

            if (len(newly_seen) > 0):
                for key in newly_seen:
                    if isinstance(key, int):
                        for box in results[0].boxes:
                            if (box.id == id):
                                cls_id = int(box.cls)
                                label = results[0].names.get(cls_id, "unknown animal")
                                await self.send_event(f"met a {label.split("-")[1]} 🐾")
                        
                    else:
                        await self.send_event(f"met {key} 👤")
            self.state.seen = current_seen







