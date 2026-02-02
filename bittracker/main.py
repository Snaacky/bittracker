from typing import Any

import bjoern

from bittracker.config import config
from bittracker.router import handle_request, register_route
from bittracker.routes.announce import announce
from bittracker.routes.stats import stats
from bittracker.scheduler import register_schedulers


def setup() -> None:
    """Registers the routes to route requests across and setup the schedulers."""
    register_route("/announce", announce)
    register_route("/stats", stats)
    register_schedulers()


def app(environ: dict[str, Any], start_response: Any) -> list[Any]:
    """Bjoern server entrypoint, passed to the router for subsequent processing."""
    status_code, body, status_message, content_type = handle_request(environ)
    start_response(f"{status_code} {status_message}", [("Content-Type", content_type)])
    return [body]


if __name__ == "__main__":
    setup()
    bjoern.run(app, config["server"]["host"], config["server"]["port"])
