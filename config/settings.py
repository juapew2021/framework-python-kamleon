import yaml
from pathlib import Path

CONFIG_FILE = (
    Path(__file__).parent / "local.yaml"
)

with open(CONFIG_FILE, "r") as file:
    config = yaml.safe_load(file)

BASE_URL = config["base_url"]