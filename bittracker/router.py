from urllib.parse import parse_qs

from bittracker.responses import Response


routes = {}


def register_route(path, func) -> None:
    """Register a function to a route for future routing"""
    routes[path] = func


def handle_request(environ) -> tuple[int, bytes, str, str]:
    """Pass the request to the respective route and return the response"""
    path = environ["PATH_INFO"]
    handler = routes.get(path)

    if not handler:
        return 404, b"Not Found", "Not Found", "text/plain"

    if environ["REQUEST_METHOD"] != "GET":
        return 405, b"Only GET allowed", "Method Not Allowed", "text/plain"

    # parse_qs returns a list for every parameter so flatten the ones that don't need to be in a list.
    params = {k: v[0] if len(v) == 1 else v for k, v in parse_qs(environ.get("QUERY_STRING", "")).items()}
    result = handler(environ, params)

    if isinstance(result, Response):
        body = result.as_wsgi()
        content_type = getattr(result, "content_type", "text/plain")
    else:
        body = result if isinstance(result, bytes) else str(result).encode("utf-8")
        content_type = "text/plain"

    return 200, body, "OK", content_type
