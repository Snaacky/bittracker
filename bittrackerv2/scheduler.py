import os
from datetime import datetime, timedelta, timezone

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from bittrackerv2.config import config
from bittrackerv2.swarms import swarms
from bittrackerv2.utils import format_bytes


def print_status() -> None:
    """Scheduler runs every 2 seconds, prints current tracker stats to console."""
    total_swarms = len(swarms.keys())
    total_peers = sum(len(swarm) for swarm in swarms.values())
    total_upload = sum(peer.uploaded for swarm in swarms.values() for peer in swarm.values())
    total_download = sum(peer.downloaded for swarm in swarms.values() for peer in swarm.values())

    os.system("clear")
    print("bittracker v0.1")
    print("-----------------------------------")
    print(f"Listening on: {config['server']['host']}:{config['server']['port']}")
    print("-----------------------------------")
    print(f"Total peers:  {total_peers}")
    print(f"Total swarms: {total_swarms}")
    print(f"Total upload: {format_bytes(total_upload)}")
    print(f"Total download: {format_bytes(total_download)}")
    print("-----------------------------------")


def prune_swarms() -> None:
    """Scheduler runs every client_dead_after seconds, prunes dead peers."""
    now = datetime.now(timezone.utc)
    inactivity_threshold = timedelta(seconds=config["tracker"]["client_dead_after"])

    for info_hash, swarm in list(swarms.items()):
        for key in list(swarm.keys()):
            peer = swarm[key]
            if now - peer.last_announce > inactivity_threshold:
                del swarm[key]

        if not swarm:
            del swarms[info_hash]


def register_schedulers() -> None:
    """Function called from app.setup() to initialize the schedulers."""
    scheduler = BackgroundScheduler()
    scheduler.add_job(print_status, trigger=IntervalTrigger(seconds=2))
    scheduler.add_job(prune_swarms, trigger=IntervalTrigger(seconds=config["tracker"]["prune_interval"]))
    scheduler.start()
