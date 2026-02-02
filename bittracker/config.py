import tomllib
from pathlib import Path


config_file = Path(__file__).parent.parent / "config.toml"
if not config_file.is_file():
    raise FileNotFoundError("Unable to find config, exiting...")

with open("config.toml", "rb") as f:
    config = tomllib.load(f)
