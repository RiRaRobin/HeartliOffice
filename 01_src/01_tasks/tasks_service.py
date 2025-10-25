# 01_src/01_tasks/tasks_service.py
# --- Bootstrap: Projekt-ROOT in sys.path bringen, Alias-Package 'src' aktivieren
from __future__ import annotations
import sys
from pathlib import Path

_CUR = Path(__file__).resolve()
_ROOT = _CUR
while _ROOT != _ROOT.parent and not (_ROOT / "path_config.py").exists():
    _ROOT = _ROOT.parent

root_str = str(_ROOT)
if root_str not in sys.path:
    sys.path.insert(0, root_str)

# Wichtig: 'src' initialisieren (lädt unser alias-Package)
import src  # noqa: F401

from pathlib import Path
from datetime import date
from typing import Any, Dict

# Pfade & IO
from path_config import DATA_TASKS_ACTIVE
from src.common.io_yaml import write_yaml # type: ignore

# ID-Generator (optional)
try:
    from src.common.ids import _next_running_number # type: ignore
    USE_IDS = True
except Exception:
    USE_IDS = False


STATUS_VALUES = ["OPEN", "READY", "DONE"]
PRIO_VALUES = [0, 1, 2, 3, 4]


def _task_file(task_id: str) -> Path:
    return DATA_TASKS_ACTIVE / f"{task_id}.yaml"


def generate_task_id(title_hint: str = "task") -> str:
    if USE_IDS:
        today = date.today().strftime("%Y-%m-%d")
        prefix = f"T-{today}"
        nr = _next_running_number(DATA_TASKS_ACTIVE, prefix)
        return f"{prefix}-{nr:03d}"
    # Fallback
    safe = "".join(c for c in title_hint if c.isalnum() or c in ("-","_")).strip() or "task"
    return f"T-{safe}"


def save_new_task(data: Dict[str, Any]) -> str:
    """Erstellt eine neue Task-YAML. Gibt die ID zurück."""
    task_id = data.get("id") or generate_task_id(data.get("beschreibung", "task"))

    payload = {
        "id": task_id,
        "beschreibung": data.get("beschreibung", "").strip(),
        "projekt": data.get("projekt", "").strip(),
        "dokument_nr": data.get("dokument_nr", "").strip(),
        "dokument_name": data.get("dokument_name", "").strip(),
        "auftrag_erhalten": data.get("auftrag_erhalten", "").strip(),  # yyyy-mm-dd
        "faellig_bis": data.get("faellig_bis", "").strip(),            # yyyy-mm-dd
        "weitere_dokumente": data.get("weitere_dokumente", []) or [],
        "notizen": data.get("notizen", ""),
        "follow_up": data.get("follow_up", ""),
        "status": data.get("status", "OPEN"),
        "dringlichkeit": int(data.get("dringlichkeit", 2) or 2),
        "verlinkte_fragen": data.get("verlinkte_fragen", []) or [],
    }
    write_yaml(_task_file(task_id), payload)
    return task_id
