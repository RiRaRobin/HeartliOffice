# 01_src/00_common/io_yaml.py
from pathlib import Path
import yaml

def read_yaml(path: Path) -> dict | list:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def write_yaml(path: Path, data) -> None:
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)
