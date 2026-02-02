from dataclasses import dataclass
from datetime import datetime
import socket
import struct

from bittracker.enums import Event


@dataclass(slots=True)
class Peer:
    peer_id: str
    ip: str
    port: int
    uploaded: int
    downloaded: int
    left: int
    last_announce: datetime
    last_event: Event | None

    def compact(self) -> bytes:
        return socket.inet_aton(self.ip) + struct.pack("!H", self.port)
