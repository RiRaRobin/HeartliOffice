# 01_src/01_tasks/__init__.py
from __future__ import annotations
import sys
from pathlib import Path
import importlib.util

# Projektwurzel -> path_config.py finden
ROOT = Path(__file__).resolve()
while ROOT.name not in (".", "/") and not (ROOT / "path_config.py").exists():
    if ROOT == ROOT.parent:
        break
    ROOT = ROOT.parent

# Pfad zur Projektwurzel in sys.path aufnehmen (für "path_config", etc.)
root_str = str(ROOT)
if root_str not in sys.path:
    sys.path.insert(0, root_str)

# Absoluter Pfad dieses nummerierten Source-Ordners
CODE_TASKS = ROOT / "01_src" / "01_tasks"

def _load_child(mod_name: str, file_path: Path):
    """Lädt eine .py-Datei als Submodul dieses Pakets (ohne normalen Paket-Baum)."""
    spec = importlib.util.spec_from_file_location(f"{__name__}.{mod_name}", file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Kann Modul {mod_name} an {file_path} nicht laden")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[f"{__name__}.{mod_name}"] = mod
    spec.loader.exec_module(mod)
    return mod

# Untermodul(e) registrieren:
_tasks_service = _load_child("tasks_service", CODE_TASKS / "tasks_service.py")

# optionale Re-Exports:
from .tasks_service import save_new_task, generate_task_id, STATUS_VALUES, PRIO_VALUES  # noqa: E402,F401

__all__ = ["tasks_service", "save_new_task", "generate_task_id", "STATUS_VALUES", "PRIO_VALUES"]
