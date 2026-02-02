from enum import Enum


class Event(Enum):
    STARTED = "started"
    STOPPED = "stopped"
    COMPLETED = "completed"
    PAUSED = "paused"
