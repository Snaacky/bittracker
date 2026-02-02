import json
from typing import Any

from bencode import bencode


class Response:
    """Generic HTTP response that encodes content to bytes and stores Content-Type."""

    def __init__(self, content: Any, content_type: str = "text/plain") -> None:
        self.content_type = content_type
        self.body = self._encode(content)

    def _encode(self, content: Any) -> bytes:
        if isinstance(content, bytes):
            return content
        elif isinstance(content, str):
            return content.encode("utf-8")
        else:
            return str(content).encode("utf-8")

    def as_wsgi(self) -> bytes:
        return self.body


class BencodeResponse(Response):
    """Response subclass that automatically bencodes content."""

    def __init__(self, content: Any) -> None:
        self.content_type = "text/plain"
        self.body = bencode(content)

    def as_wsgi(self) -> bytes:
        return self.body


class JSONResponse(Response):
    """Response subclass that automatically JSON serializes content."""

    def __init__(self, content: Any, *, indent: int | None = None) -> None:
        self.content_type = "application/json"
        self.body = self._json_encode(content, indent)

    def _json_encode(self, content: Any, indent: int | None) -> bytes:
        return json.dumps(content, indent=indent).encode("utf-8")

    def as_wsgi(self) -> bytes:
        return self.body
