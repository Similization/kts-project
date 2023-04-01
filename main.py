from pathlib import Path

import yaml
from aiohttp.web import run_app

from kts_backend.web.app import setup_app

if __name__ == "__main__":
    config = yaml.safe_load(Path("etc/config.yaml").read_text())
    run_app(app=setup_app(config=config), host="localhost", port=8080)
