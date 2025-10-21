# 01_src/00_common/ids.py
from datetime import datetime
from pathlib import Path

def _next_running_number(dir_path: Path, prefix_date: str) -> int:
    """
    Sucht in dir_path nach Dateien, die mit <prefix_date> beginnen,
    extrahiert die letzte laufende Nummer und erhöht sie um 1.
    Erwartet Dateinamen wie T-YYYY-MM-DD-001.yaml
    """
    highest = 0
    if not dir_path.exists():
        return 1
    for p in dir_path.glob("*.yaml"):
        name = p.stem  # ohne .yaml
        if name.startswith(prefix_date):
            # erwartet "T-YYYY-MM-DD-###" / "M-..." / "Q-..."
            parts = name.split("-")
            if parts and parts[-1].isdigit():
                highest = max(highest, int(parts[-1]))
    return highest + 1

def new_id(kind: str, storage_dir: Path) -> str:
    """
    kind in {"T","M","Q"} → Task/Meeting/Question
    storage_dir = Zielordner (z. B. TASKS_ACTIVE)
    """
    today = datetime.now().strftime("%Y-%m-%d")
    prefix_date = f"{kind}-{today}"
    nr = _next_running_number(storage_dir, prefix_date)
    return f"{prefix_date}-{nr:03d}"
