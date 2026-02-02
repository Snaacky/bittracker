from bittracker.config import config
from bittracker.responses import JSONResponse


def admin(environ: dict, params: dict) -> JSONResponse:
    return JSONResponse(
        {
            "server": {
                "host": config["server"]["host"],
                "port": config["server"]["port"],
            },
            "database": {
                "uri": config["database"]["uri"],
            },
            "tracker": {
                "interval": config["tracker"]["interval"],
                "min_interval": config["tracker"]["min_interval"],
                "prune_interval": config["tracker"]["prune_interval"],
                "client_dead_after": config["tracker"]["client_dead_after"],
                "swarm_peer_limit": config["tracker"]["swarm_peer_limit"],
            },
        }
    )
