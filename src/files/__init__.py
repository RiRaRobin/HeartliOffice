"""
src.common
Alias-Loader für alle Module im Ordner 01_src/00_common.
Erlaubt Imports wie:
    from src.common.io_yaml import read_yaml
    from src.common.ids import new_id
"""

import sys
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
from path_config import CODE_FILES  # Pfad: project_root/01_src/00_common


def _load_child(mod_name: str, file_path: Path):
    """
    Lädt eine Python-Datei als Submodul (z. B. io_yaml.py → src.common.io_yaml).
    Registriert das Modul in sys.modules, damit es per Import auffindbar ist.
    """
    qualname = f"{__name__}.{mod_name}"
    spec = spec_from_file_location(qualname, file_path)
    mod = module_from_spec(spec)
    sys.modules[qualname] = mod
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


__all__ = []

for pyfile in CODE_FILES.glob("*.py"):
    # __init__.py selbst überspringen
    if pyfile.name == "__init__.py":
        continue

    mod_name = pyfile.stem  # Dateiname ohne .py
    try:
        _load_child(mod_name, pyfile)
        __all__.append(mod_name)
    except Exception as e:
        print(f"⚠️ Fehler beim Laden von {mod_name}: {e}")
