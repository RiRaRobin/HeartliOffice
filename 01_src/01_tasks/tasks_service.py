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
from path_config import DATA_TASKS_ACTIVE, DATA_TASKS_ARCHIVE
from src.common.io_yaml import write_yaml, read_yaml # type: ignore
# from dateutil.parser import parse as parse_date

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

def _int_or_default(val, default=2) -> int:
    if val is None:
        return default
    try:
        s = str(val).strip()
        if s == "":
            return default
        return int(s)
    except Exception:
        return default

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
        "dringlichkeit": _int_or_default(data.get("dringlichkeit"), 2),
        "verlinkte_fragen": data.get("verlinkte_fragen", []) or [],
    }
    write_yaml(_task_file(task_id), payload)
    return task_id


def _normalize_task(t: dict) -> dict:
    return {
        "id": t.get("id", ""),
        "beschreibung": t.get("beschreibung", ""),
        "projekt": t.get("projekt", ""),

        # 🔧 Wichtige Felder ergänzen:
        "dokument_nr": t.get("dokument_nr", ""),
        "dokument_name": t.get("dokument_name", ""),
        "auftrag_erhalten": t.get("auftrag_erhalten", ""),  # <-- fehlte bisher
        "faellig_bis": t.get("faellig_bis", ""),

        "weitere_dokumente": t.get("weitere_dokumente", []) or [],
        "notizen": t.get("notizen", ""),
        "follow_up": t.get("follow_up", ""),

        "status": t.get("status", "OPEN"),
        "dringlichkeit": _int_or_default(t.get("dringlichkeit"), 2),
        "verlinkte_fragen": t.get("verlinkte_fragen", []) or [],
    }

def load_tasks_active() -> list[dict]:
    DATA_TASKS_ACTIVE.mkdir(parents=True, exist_ok=True)  # <— Verzeichnis sicherstellen
    rows: list[dict] = []
    for f in sorted(DATA_TASKS_ACTIVE.glob("*.yaml")):
        try:
            t = read_yaml(f) or {}
            rows.append(_normalize_task(t))
        except Exception as e:
            print(f"[WARN] Konnte {f.name} nicht laden: {e}")
    rows.sort(key=lambda r: r.get("id", ""))
    return rows

def load_task(task_id: str) -> dict:
    """Einzelnen Task laden (normalisiert)."""
    p = _task_file(task_id)
    if not p.exists():
        raise FileNotFoundError(task_id)
    t = read_yaml(p) or {}
    return _normalize_task(t)

def save_existing_task(task_id: str, data: Dict[str, Any]) -> str:
    """Bestehenden Task (selbe ID) überschreiben/aktualisieren."""
    payload = {
        "id": task_id,
        "beschreibung": (data.get("beschreibung","") or "").strip(),
        "projekt": (data.get("projekt","") or "").strip(),
        "dokument_nr": (data.get("dokument_nr","") or "").strip(),
        "dokument_name": (data.get("dokument_name","") or "").strip(),
        "auftrag_erhalten": (data.get("auftrag_erhalten","") or "").strip(),
        "faellig_bis": (data.get("faellig_bis","") or "").strip(),
        "weitere_dokumente": data.get("weitere_dokumente", []) or [],
        "notizen": data.get("notizen","") or "",
        "follow_up": data.get("follow_up","") or "",
        "status": data.get("status","OPEN") or "OPEN",
        "dringlichkeit": _int_or_default(data.get("dringlichkeit"), 2),
        "verlinkte_fragen": data.get("verlinkte_fragen", []) or [],
    }
    write_yaml(_task_file(task_id), payload)
    return task_id

def archive_task(task_id: str) -> None:
    """Verschiebt eine Task-YAML von active → archive. Überschreibt ggf. vorhandene gleichnamige Datei."""
    src = _task_file(task_id)
    if not src.exists():
        raise FileNotFoundError(f"Task {task_id} nicht gefunden: {src}")

    DATA_TASKS_ARCHIVE.mkdir(parents=True, exist_ok=True)
    dst = DATA_TASKS_ARCHIVE / f"{task_id}.yaml"

    # Falls im Archiv bereits vorhanden: überschreiben (oder hier alternative Logik einbauen)
    dst.write_bytes(src.read_bytes())
    src.unlink()
