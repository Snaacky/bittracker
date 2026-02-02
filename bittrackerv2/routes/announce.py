from datetime import datetime, timezone
from itertools import islice

from bittrackerv2.config import config
from bittrackerv2.entities import Peer
from bittrackerv2.enums import Event
from bittrackerv2.responses import BencodeResponse
from bittrackerv2.swarms import swarms


def announce(environ: dict, params: dict) -> BencodeResponse:
    # Normalize the parameters from the request for future reference.
    ip = environ.get("REMOTE_ADDR", "127.0.0.1")
    port = int(params.get("port", 0))
    info_hash = params.get("info_hash")
    peer_id = params.get("peer_id")
    compact = bool(int(params.get("compact", 0)))
    uploaded = int(params.get("uploaded", 0))
    downloaded = int(params.get("downloaded", 0))
    left = int(params.get("left", 0))
    numwant = int(params.get("numwant", 0))
    event = params.get("event")
    now = datetime.now(timezone.utc)

    # Verify that info_hash, peer_id, and port are all valid.
    if not info_hash or not peer_id or not port or port <= 0 or port > 65535:
        return BencodeResponse(
            {
                "failure reason": "malformed announce",
                "interval": config["tracker"]["interval"],
                "min interval": config["tracker"]["min_interval"],
                "external ip": ip,
            }
        )

    # Sanity check the number of peers requested and cap it if invalid.
    if numwant <= 0 or numwant > 200:
        numwant = config["tracker"]["swarm_peer_limit"]

    # Attempt to fetch the peer in the swarm.
    swarm = swarms[info_hash]
    key = (ip, port, peer_id)
    peer = swarm.get(key)

    if not peer and event is not Event.STOPPED:
        peer = Peer(
            peer_id=peer_id,
            ip=ip,
            port=port,
            uploaded=uploaded,
            downloaded=downloaded,
            left=left,
            last_event=event,
            last_announce=now,
        )
        swarm[key] = peer
    elif peer and event is not Event.STOPPED:
        if uploaded:
            peer.uploaded += uploaded
        if downloaded:
            peer.downloaded += downloaded
        if left:
            peer.left = left
        if event:
            peer.last_event = event
        peer.last_announce = now
    elif peer and event is Event.STOPPED:
        swarm.pop(key, None)

    # Return without a peer list if the event was paused or stopped.
    if event in {Event.PAUSED, Event.STOPPED}:
        return BencodeResponse(
            {
                "peers": b"" if compact else [],
                "interval": config["tracker"]["interval"],
                "min interval": config["tracker"]["min_interval"],
                "external ip": ip,
            }
        )

    # Otherwise, return a valid peer list.
    return BencodeResponse(
        {
            "peers": fetch_swarm_peers(swarm=swarm, compact=compact, limit=numwant),
            "interval": config["tracker"]["interval"],
            "min interval": config["tracker"]["min_interval"],
            "external ip": ip,
        }
    )


def fetch_swarm_peers(swarm: dict, compact: bool, limit: int) -> bytes | list:
    limit = min(
        limit or config["tracker"]["swarm_peer_limit"],
        config["tracker"]["swarm_peer_limit"],
    )
    skip_events = {Event.PAUSED, Event.STOPPED}
    sliced = islice(swarm.values(), limit)

    if compact:
        return b"".join(peer.compact() for peer in sliced if peer.last_event not in skip_events)
    else:
        return [{"ip": peer.ip, "port": peer.port} for peer in sliced if peer.last_event not in skip_events]
