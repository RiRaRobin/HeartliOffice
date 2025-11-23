# 01_src/04_files/files_service.py
from __future__ import annotations

import sys
from pathlib import Path
from datetime import date, datetime
from typing import Any, Dict, List, Optional

# --- Bootstrap: Projekt-ROOT & src-Alias ---
_CUR = Path(__file__).resolve()
_ROOT = _CUR
while _ROOT != _ROOT.parent and not (_ROOT / "path_config.py").exists():
    _ROOT = _ROOT.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
import src  # noqa: F401

from path_config import DATA_FILES_ACTIVE, DATA_FILES_ARCHIVE  # type: ignore
from src.common.io_yaml import read_yaml, write_yaml          # type: ignore

# ID-Generator (wie bei Tasks)
try:
    from src.common.ids import _next_running_number  # type: ignore
    USE_IDS = True
except Exception:
    USE_IDS = False


FILE_TYPE_VALUES = ["BU", "PFAD"]


def _ensure_dirs() -> None:
    """Stellt sicher, dass Active-/Archive-Ordner existieren."""
    DATA_FILES_ACTIVE.mkdir(parents=True, exist_ok=True)
    DATA_FILES_ARCHIVE.mkdir(parents=True, exist_ok=True)


def _file_path(file_id: str, archive: bool = False) -> Path:
    """Dateipfad für eine File-ID (active oder archive)."""
    base = DATA_FILES_ARCHIVE if archive else DATA_FILES_ACTIVE
    return base / f"{file_id}.yaml"


def generate_file_id(title_hint: str = "file") -> str:
    """Erzeugt eine neue File-ID, z.B. F-2025-10-26-001."""
    if USE_IDS:
        today = date.today().strftime("%Y-%m-%d")
        prefix = f"F-{today}"
        nr = _next_running_number(DATA_FILES_ACTIVE, prefix)
        return f"{prefix}-{nr:03d}"
    # Fallback: aus Name / Hinweis
    safe = "".join(c for c in title_hint if c.isalnum() or c in ("-","_")).strip() or "file"
    return f"F-{safe}"


def _now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def normalize_file(data: Dict[str, Any]) -> Dict[str, Any]:
    """Sorgt für vollständige Keys & sinnvolle Defaults."""
    return {
        "id": data.get("id", ""),
        "projekt": data.get("projekt", "").strip(),
        "typ": (data.get("typ") or "BU").strip().upper(),     # "BU" oder "PFAD"
        "ref": data.get("ref", "").strip(),                   # BU-Nr oder Pfad
        "name": data.get("name", "").strip(),
        "beschreibung": data.get("beschreibung", ""),
        "tags": data.get("tags", []) or [],
        "notizen": data.get("notizen", ""),
        # Graph-Infos (immer als Liste von IDs):
        "links_in": data.get("links_in", []) or [],
        "links_out": data.get("links_out", []) or [],
        "created_at": data.get("created_at", ""),
        "updated_at": data.get("updated_at", ""),
    }


def load_files_active() -> List[Dict[str, Any]]:
    """Lädt alle aktiven Files (aus DATA_FILES_ACTIVE)."""
    _ensure_dirs()
    rows: List[Dict[str, Any]] = []
    for f in sorted(DATA_FILES_ACTIVE.glob("*.yaml")):
        try:
            d = read_yaml(f) or {}
            rows.append(normalize_file(d))
        except Exception as e:
            print(f"[WARN] Konnte File {f.name} nicht laden: {e}")
    return rows


def load_file(file_id: str, archive: bool = False) -> Optional[Dict[str, Any]]:
    """Lädt ein einzelnes File per ID (active oder archive)."""
    p = _file_path(file_id, archive=archive)
    if not p.exists():
        return None
    try:
        d = read_yaml(p) or {}
        return normalize_file(d)
    except Exception as e:
        print(f"[WARN] Konnte File {file_id} nicht laden: {e}")
        return None


def save_new_file(data: Dict[str, Any]) -> str:
    """Erstellt ein neues File-YAML, gibt die ID zurück."""
    _ensure_dirs()
    file_id = data.get("id") or generate_file_id(data.get("name", "file"))

    now = _now_str()
    payload = normalize_file({
        **data,
        "id": file_id,
        "created_at": data.get("created_at") or now,
        "updated_at": now,
    })
    write_yaml(_file_path(file_id), payload)
    return file_id


def save_existing_file(file_id: str, data: Dict[str, Any]) -> str:
    """Aktualisiert ein bestehendes File-YAML (nur Active-Bereich)."""
    _ensure_dirs()
    old = load_file(file_id) or {"id": file_id}
    now = _now_str()
    payload = normalize_file({
        **old,
        **data,
        "id": file_id,
        "updated_at": now,
        "created_at": old.get("created_at") or now,
    })
    write_yaml(_file_path(file_id), payload)
    return file_id


def archive_file(file_id: str) -> None:
    """Verschiebt ein File von Active nach Archive (YAML umkopieren)."""
    _ensure_dirs()
    src = _file_path(file_id, archive=False)
    dst = _file_path(file_id, archive=True)
    if not src.exists():
        raise FileNotFoundError(file_id)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(src.read_bytes())
    src.unlink(missing_ok=True)


# ------------------------------
# Link-Management (Abhängigkeiten)
# ------------------------------

def add_link(source_id: str, target_id: str) -> None:
    """
    Fügt eine gerichtete Kante source -> target hinzu:
        source.links_out += [target]
        target.links_in  += [source]
    """
    src = load_file(source_id)
    tgt = load_file(target_id)
    if not src or not tgt:
        raise ValueError(f"Unbekanntes File in add_link: {source_id=} {target_id=}")

    if target_id not in src.get("links_out", []):
        src["links_out"] = (src.get("links_out") or []) + [target_id]
    if source_id not in tgt.get("links_in", []):
        tgt["links_in"] = (tgt.get("links_in") or []) + [source_id]

    save_existing_file(source_id, src)
    save_existing_file(target_id, tgt)


def remove_link(source_id: str, target_id: str) -> None:
    """Entfernt die gerichtete Kante source -> target in beiden Richtungen."""
    src = load_file(source_id)
    tgt = load_file(target_id)
    if not src or not tgt:
        return

    src["links_out"] = [x for x in (src.get("links_out") or []) if x != target_id]
    tgt["links_in"] = [x for x in (tgt.get("links_in") or []) if x != source_id]

    save_existing_file(source_id, src)
    save_existing_file(target_id, tgt)


def files_by_project(projekt: str) -> List[Dict[str, Any]]:
    """Filtert aktive Files auf ein bestimmtes Projekt."""
    projekt = (projekt or "").strip()
    if not projekt:
        return load_files_active()
    return [f for f in load_files_active() if (f.get("projekt") or "").strip() == projekt]


# ------------------------------
# Suche & Anzeige-Labels (für GUI / Links)
# ------------------------------

def file_label(file_data: Dict[str, Any]) -> str:
    """
    Erzeugt einen hübschen Text für GUI-Dropdowns, z.B.:
        "[BU-12345] Systemarchitektur"
        "[PFAD] Z:\\Projekte\\..."
    """
    typ = (file_data.get("typ") or "").upper()
    ref = file_data.get("ref", "")
    name = file_data.get("name", "")

    if ref and name:
        return f"[{ref}] {name}"
    if ref:
        return f"[{ref}]"
    if name:
        return name
    return file_data.get("id", "<ohne ID>")


def search_files_for_link_input(
    text: str,
    projekt: Optional[str] = None,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    """
    Liefert eine Liste von Files, die zu 'text' passen.
    Sucht in:
        - ref (BU-Nr oder Pfad)
        - name
        - beschreibung
    Optional gefiltert nach Projekt.
    Rückgabe: Dicts mit id, label, projekt, typ, ref, name
    """
    q = (text or "").strip().lower()
    if not q:
        return []

    rows = load_files_active()

    if projekt:
        p = projekt.strip().lower()
        rows = [r for r in rows if (r.get("projekt") or "").strip().lower() == p]

    res: List[Dict[str, Any]] = []
    for r in rows:
        blob = " ".join([
            r.get("ref", ""),
            r.get("name", ""),
            r.get("beschreibung", ""),
        ]).lower()
        if q in blob:
            res.append({
                "id": r.get("id", ""),
                "label": file_label(r),
                "projekt": r.get("projekt", ""),
                "typ": r.get("typ", ""),
                "ref": r.get("ref", ""),
                "name": r.get("name", ""),
            })
        if len(res) >= limit:
            break

    return res
