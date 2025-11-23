# 01_src/04_files/files_service.py
from __future__ import annotations

# --- Bootstrap: Projekt-ROOT & Alias-Package 'src' aktivieren
import sys
from pathlib import Path

_CUR = Path(__file__).resolve()
_ROOT = _CUR
while _ROOT != _ROOT.parent and not (_ROOT / "path_config.py").exists():
    _ROOT = _ROOT.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
import src  # noqa: F401

from datetime import datetime
from typing import Any, Dict, List

from path_config import DATA_FILES
from src.common.io_yaml import read_yaml, write_yaml  # type: ignore
try:
    from src.common.ids import _next_running_number  # type: ignore
    USE_IDS = True
except Exception:
    USE_IDS = False


# Wir machen analog zu Tasks zwei Unterordner:
DATA_FILES_ACTIVE = DATA_FILES / "01_active"
DATA_FILES_ARCHIVE = DATA_FILES / "02_archive"
DATA_FILES_ACTIVE.mkdir(parents=True, exist_ok=True)
DATA_FILES_ARCHIVE.mkdir(parents=True, exist_ok=True)


def _file_path_active(file_id: str) -> Path:
    return DATA_FILES_ACTIVE / f"{file_id}.yaml"


def _file_path_archive(file_id: str) -> Path:
    return DATA_FILES_ARCHIVE / f"{file_id}.yaml"


def generate_file_id(name_hint: str = "file") -> str:
    """Erzeugt eine laufende F-ID."""
    if USE_IDS:
        today = datetime.now().strftime("%Y-%m-%d")
        prefix = f"F-{today}"
        nr = _next_running_number(DATA_FILES_ACTIVE, prefix)
        return f"{prefix}-{nr:03d}"

    safe = "".join(c for c in name_hint if c.isalnum() or c in ("-", "_")).strip() or "file"
    return f"F-{safe}"


def save_new_file(data: Dict[str, Any]) -> str:
    """
    Legt ein neues File-YAML an und gibt die ID zurück.
    Erwartete Felder in data:
      name, ref, projekt, typ, beschreibung, tags, notizen,
      links_in, links_out
    """
    file_id = data.get("id") or generate_file_id(data.get("name", "file"))
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    payload = {
        "id": file_id,
        "projekt": data.get("projekt", "").strip(),
        "typ": (data.get("typ", "") or "BU").strip(),  # "BU" oder "PFAD"
        "ref": data.get("ref", "").strip(),           # BU-Nr oder Pfad
        "name": data.get("name", "").strip(),
        "beschreibung": data.get("beschreibung", "").strip(),
        "tags": data.get("tags", []) or [],
        "notizen": data.get("notizen", "").strip(),
        "links_in": data.get("links_in", []) or [],
        "links_out": data.get("links_out", []) or [],
        "created_at": now,
        "updated_at": now,
    }
    write_yaml(_file_path_active(file_id), payload)
    return file_id


def save_existing_file(file_id: str, data: Dict[str, Any]) -> str:
    """
    Aktualisiert ein bestehendes File-YAML.
    created_at bleibt erhalten, updated_at wird angepasst.
    """
    path = _file_path_active(file_id)
    if path.exists():
        existing = read_yaml(path)
    else:
        existing = {"id": file_id, "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

    created_at = existing.get("created_at") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    payload = {
        "id": file_id,
        "projekt": data.get("projekt", existing.get("projekt", "")).strip(),
        "typ": (data.get("typ", existing.get("typ", "BU")) or "BU").strip(),
        "ref": data.get("ref", existing.get("ref", "")).strip(),
        "name": data.get("name", existing.get("name", "")).strip(),
        "beschreibung": data.get("beschreibung", existing.get("beschreibung", "")).strip(),
        "tags": data.get("tags", existing.get("tags", []) or []),
        "notizen": data.get("notizen", existing.get("notizen", "")).strip(),
        "links_in": data.get("links_in", existing.get("links_in", []) or []),
        "links_out": data.get("links_out", existing.get("links_out", []) or []),
        "created_at": created_at,
        "updated_at": now,
    }
    write_yaml(path, payload)
    return file_id


def load_files_active() -> List[Dict[str, Any]]:
    """Lädt alle aktiven Files als Liste von Dicts."""
    rows: List[Dict[str, Any]] = []
    for f in sorted(DATA_FILES_ACTIVE.glob("*.yaml")):
        try:
            d = read_yaml(f)
            if isinstance(d, dict):
                rows.append(d)
        except Exception as e:
            print(f"[WARN] Konnte {f.name} nicht laden: {e}")
    return rows


def load_file(file_id: str) -> Dict[str, Any] | None:
    """Ein einzelnes File laden (oder None)."""
    p = _file_path_active(file_id)
    if not p.exists():
        return None
    try:
        d = read_yaml(p)
        if isinstance(d, dict):
            return d
    except Exception as e:
        print(f"[WARN] Konnte {p.name} nicht laden: {e}")
    return None


def archive_file(file_id: str) -> bool:
    """Verschiebt ein File nach 02_archive. Rückgabe: True bei Erfolg."""
    src = _file_path_active(file_id)
    if not src.exists():
        return False
    dst = _file_path_archive(file_id)
    dst.parent.mkdir(parents=True, exist_ok=True)
    src.replace(dst)
    return True
