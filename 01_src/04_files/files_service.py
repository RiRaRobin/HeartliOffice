# 01_src/04_files/files_service.py
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime, date

# --- Bootstrap: Projekt-ROOT & src-Alias finden ---
_CUR = Path(__file__).resolve()
_ROOT = _CUR
while _ROOT != _ROOT.parent and not (_ROOT / "path_config.py").exists():
    _ROOT = _ROOT.parent

if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import src  # noqa: F401

# --- Projekt-Pfade & IO-Helfer ---
from path_config import DATA_FILES_ACTIVE, DATA_FILES_ARCHIVE
from src.common.io_yaml import read_yaml, write_yaml  # type: ignore

# Optionaler ID-Generator
try:
    from src.common.ids import _next_running_number  # type: ignore
    USE_IDS = True
except Exception:
    USE_IDS = False


# ---------------------------------------------------------
# Pfad-Helfer
# ---------------------------------------------------------
def _file_path(file_id: str, active: bool = True) -> Path:
    base = DATA_FILES_ACTIVE if active else DATA_FILES_ARCHIVE
    return base / f"{file_id}.yaml"


# ---------------------------------------------------------
# ID-Generator
# ---------------------------------------------------------
def generate_file_id(name_hint: str = "file") -> str:
    """Neue File-ID, z.B. F-2025-10-26-001."""
    if USE_IDS:
        today = date.today().strftime("%Y-%m-%d")
        prefix = f"F-{today}"
        nr = _next_running_number(DATA_FILES_ACTIVE, prefix)
        return f"{prefix}-{nr:03d}"

    safe = "".join(c for c in name_hint if c.isalnum() or c in ("-", "_")).strip() or "file"
    return f"F-{safe}"


# ---------------------------------------------------------
# Speichern (neu / bestehend)
# ---------------------------------------------------------
def save_new_file(data: Dict[str, Any]) -> str:
    """Legt ein neues File im ACTIVE-Ordner an und gibt die ID zurück."""
    DATA_FILES_ACTIVE.mkdir(parents=True, exist_ok=True)

    file_id = data.get("id") or generate_file_id(data.get("name", "file"))
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    payload: Dict[str, Any] = {
        "id": file_id,
        "projekt": (data.get("projekt") or "").strip(),
        "typ": data.get("typ", "BU"),
        "ref": (data.get("ref") or "").strip(),           # BU-Nr oder Pfad
        "name": (data.get("name") or "").strip(),
        "beschreibung": data.get("beschreibung", ""),
        "tags": data.get("tags") or [],
        "notizen": data.get("notizen", ""),
        "links_in": data.get("links_in") or [],
        "links_out": data.get("links_out") or [],
        "created_at": data.get("created_at") or now,
        "updated_at": now,
    }

    write_yaml(_file_path(file_id, active=True), payload)
    return file_id


def save_existing_file(file_id: str, data: Dict[str, Any]) -> str:
    """
    Überschreibt ein bestehendes File (ACTIVE).
    created_at bleibt erhalten, updated_at wird auf jetzt gesetzt.
    """
    DATA_FILES_ACTIVE.mkdir(parents=True, exist_ok=True)
    path = _file_path(file_id, active=True)

    existing: Dict[str, Any] = {}
    try:
        existing = read_yaml(path) or {}
    except Exception:
        existing = {}

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    created = existing.get("created_at") or data.get("created_at")

    payload: Dict[str, Any] = {
        "id": file_id,
        "projekt": (data.get("projekt") or existing.get("projekt", "")).strip(),
        "typ": data.get("typ", existing.get("typ", "BU")),
        "ref": (data.get("ref") or existing.get("ref", "")).strip(),
        "name": (data.get("name") or existing.get("name", "")).strip(),
        "beschreibung": data.get("beschreibung", existing.get("beschreibung", "")),
        "tags": data.get("tags", existing.get("tags", [])),
        "notizen": data.get("notizen", existing.get("notizen", "")),
        "links_in": data.get("links_in", existing.get("links_in", [])),
        "links_out": data.get("links_out", existing.get("links_out", [])),
        "created_at": created or now,
        "updated_at": now,
    }

    write_yaml(path, payload)
    return file_id


# ---------------------------------------------------------
# Laden & Filtern
# ---------------------------------------------------------
def load_files_active(
    project: Optional[str] = None,
    search: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Lädt alle aktiven Files als Dict-Liste.
    Optional Filter:
      - project: nur Files mit genau diesem Projekt
      - search: Text-Suche in id, name, ref, beschreibung, projekt
    """
    DATA_FILES_ACTIVE.mkdir(parents=True, exist_ok=True)

    search = (search or "").strip().lower()
    rows: List[Dict[str, Any]] = []

    for f in sorted(DATA_FILES_ACTIVE.glob("*.yaml")):
        try:
            data = read_yaml(f) or {}
        except Exception as e:
            print(f"[WARN] Konnte {f.name} nicht laden: {e}")
            continue

        if project and data.get("projekt") != project:
            continue

        if search:
            hay = " ".join(
                str(data.get(k, ""))
                for k in ("id", "name", "ref", "beschreibung", "projekt")
            ).lower()
            if search not in hay:
                continue

        rows.append(data)

    # Standard: nach ID sortiert
    rows.sort(key=lambda d: d.get("id", ""))
    return rows


# ---------------------------------------------------------
# Archivieren
# ---------------------------------------------------------
def archive_file(file_id: str) -> bool:
    """Verschiebt ein File von ACTIVE nach ARCHIVE. Gibt True/False zurück."""
    src_p = _file_path(file_id, active=True)
    if not src_p.exists():
        return False

    DATA_FILES_ARCHIVE.mkdir(parents=True, exist_ok=True)
    dst_p = _file_path(file_id, active=False)
    src_p.replace(dst_p)
    return True


# ---------------------------------------------------------
# IDs für QCompleter
# ---------------------------------------------------------
def load_all_file_ids() -> List[str]:
    """
    Liefert alle File-IDs aus ACTIVE (ohne Duplikate, sortiert).
    Wird vom QCompleter im FileDialog verwendet.
    """
    DATA_FILES_ACTIVE.mkdir(parents=True, exist_ok=True)

    ids: set[str] = set()
    for f in DATA_FILES_ACTIVE.glob("*.yaml"):
        try:
            data = read_yaml(f) or {}
        except Exception:
            continue
        fid = str(data.get("id") or "").strip()
        if fid:
            ids.add(fid)

    return sorted(ids)

def load_file(file_id: str) -> Dict[str, Any] | None:
    """
    Lädt ein einzelnes File aus ACTIVE.
    Gibt ein Dict zurück oder None, wenn die Datei nicht gefunden/lesbar ist.
    """
    path = _file_path(file_id, active=True)
    if not path.exists():
        return None
    try:
        return read_yaml(path) or {}
    except Exception as e:
        print(f"[WARN] Konnte File {file_id} nicht laden: {e}")
        return None
