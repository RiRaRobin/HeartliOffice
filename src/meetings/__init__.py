import sys
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
from path_config import CODE_MEETINGS  # Pfad: 01_src/01_tasks

def _load_child(mod_name: str, file_path: Path):
    qualname = f"{__name__}.{mod_name}"
    spec = spec_from_file_location(qualname, file_path)
    mod = module_from_spec(spec)
    sys.modules[qualname] = mod
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


__all__ = []
for pyfile in CODE_MEETINGS.glob("*.py"):
    if pyfile.name == "__init__.py":
        continue
    mod_name = pyfile.stem
    try:
        _load_child(mod_name, pyfile)
        __all__.append(mod_name)
    except Exception as e:
        print(f"⚠️ Fehler beim Laden von {mod_name}: {e}")
