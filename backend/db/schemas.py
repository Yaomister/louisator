from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime

class Session(BaseModel):
    id: UUID4
    start_time: datetime
    end_time: Optional[datetime] = None


class State(BaseModel):
    session_id: UUID4
    timestamp: datetime
    movement_speed: int # m/s
    energy: float
    activity: str

class Event(BaseModel):
    session_id: UUID4
    timestamp: datetime
    type: str
    description: str

