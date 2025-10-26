# 01_src/03_questions/questions_service.py
from __future__ import annotations
from pathlib import Path
from datetime import date
from typing import Any, Dict, List

from path_config import DATA_QUESTIONS_ACTIVE, DATA_QUESTIONS_ARCHIVE
from src.common.io_yaml import read_yaml, write_yaml # type: ignore

# optional: IDs wie bei Tasks
try:
    from src.common.ids import _next_running_number # type: ignore
    USE_IDS = True
except Exception:
    USE_IDS = False

STATUS = ["OPEN", "CLOSED"]
TYPES  = ["FRAGE", "INFO"]

def _ensure_dirs() -> None:
    DATA_QUESTIONS_ACTIVE.mkdir(parents=True, exist_ok=True)
    DATA_QUESTIONS_ARCHIVE.mkdir(parents=True, exist_ok=True)

def _q_file_active(qid: str) -> Path:
    return DATA_QUESTIONS_ACTIVE / f"{qid}.yaml"

def _q_file_archive(qid: str) -> Path:
    return DATA_QUESTIONS_ARCHIVE / f"{qid}.yaml"

def _normalize(q: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": q.get("id",""),
        "person": q.get("person",""),
        "frage": q.get("frage",""),
        "status": q.get("status","OPEN"),
        "typ": q.get("typ","FRAGE"),
        "linked_task_id": q.get("linked_task_id",""),
        "created_at": q.get("created_at",""),
        "closed_at": q.get("closed_at",""),
        "notes": q.get("notes",""),
    }

def load_questions_active() -> List[Dict[str, Any]]:
    _ensure_dirs()
    rows: List[Dict[str, Any]] = []
    for f in sorted(DATA_QUESTIONS_ACTIVE.glob("*.yaml")):
        try:
            rows.append(_normalize(read_yaml(f) or {}))
        except Exception as e:
            print(f"[WARN] Frage {f.name} nicht ladbar: {e}")
    return rows

def generate_qid(title_hint: str = "q") -> str:
    today = date.today().strftime("%Y-%m-%d")
    prefix = f"Q-{today}"
    if USE_IDS:
        nr = _next_running_number(DATA_QUESTIONS_ACTIVE, prefix)
        return f"{prefix}-{nr:03d}"
    return f"{prefix}-001"

def save_new_question(data: Dict[str, Any]) -> str:
    """Neue Frage anlegen (ACTIVE) und ID zurückgeben."""
    _ensure_dirs()
    qid = data.get("id") or generate_qid(data.get("frage","q"))
    payload = _normalize({
        "id": qid,
        "person": (data.get("person","") or "").strip(),
        "frage": (data.get("frage","") or "").strip(),
        "status": data.get("status","OPEN"),
        "typ": data.get("typ","FRAGE"),
        "linked_task_id": (data.get("linked_task_id","") or "").strip(),
        "created_at": data.get("created_at") or date.today().strftime("%Y-%m-%d"),
        "closed_at": data.get("closed_at",""),
        "notes": data.get("notes",""),
    })
    write_yaml(_q_file_active(qid), payload)
    return qid

def close_question(qid: str) -> None:
    """Status CLOSED setzen (bleibt in ACTIVE; optional später archivieren)."""
    p = _q_file_active(qid)
    if not p.exists():
        raise FileNotFoundError(qid)
    cur = _normalize(read_yaml(p) or {})
    cur["status"] = "CLOSED"
    cur["closed_at"] = date.today().strftime("%Y-%m-%d")
    write_yaml(p, cur)

def archive_question(qid: str) -> None:
    """Frage nach ARCHIVE verschieben."""
    _ensure_dirs()
    src = _q_file_active(qid)
    if not src.exists():
        raise FileNotFoundError(qid)
    dst = _q_file_archive(qid)
    dst.write_bytes(src.read_bytes())
    src.unlink()
