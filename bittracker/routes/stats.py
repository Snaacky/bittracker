from bittracker.enums import Event
from bittracker.responses import JSONResponse
from bittracker.swarms import swarms


def stats(environ: dict, params: dict) -> JSONResponse:
    total_peers = 0
    total_seeders = 0
    total_leechers = 0
    total_paused = 0
    total_uploaded = 0
    total_downloaded = 0

    for swarm in swarms.values():
        total_peers += len(swarm)
        for peer in swarm.values():
            if peer.last_event == Event.COMPLETED:
                total_seeders += 1
            elif peer.last_event == Event.STARTED:
                total_leechers += 1
            elif peer.last_event == Event.PAUSED:
                total_paused += 1

            total_uploaded += peer.uploaded
            total_downloaded += peer.downloaded

    return JSONResponse(
        {
            "peers": total_peers,
            "swarms": len(swarms),
            "seeders": total_seeders,
            "leechers": total_leechers,
            "paused": total_paused,
            "uploaded": total_uploaded,
            "downloaded": total_downloaded,
        }
    )
