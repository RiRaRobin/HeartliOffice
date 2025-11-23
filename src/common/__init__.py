"""
src.common
Alias-Loader für alle Module im Ordner 01_src/00_common.

Erlaubt u.a.:
    from src.common.io_yaml import read_yaml
    from src.common.ids import _next_running_number

Alle .py-Dateien in 01_src/00_common werden automatisch als
Submodule geladen, z.B.:
    01_src/00_common/io_yaml.py  -> src.common.io_yaml
    01_src/00_common/ids.py      -> src.common.ids
"""

from __future__ import annotations

import sys
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path

# --- Projekt-ROOT anhand path_config.py finden (selbstständig, ohne path_config zu importieren) ---
_THIS = Path(__file__).resolve()
_ROOT = _THIS
while _ROOT != _ROOT.parent and not (_ROOT / "path_config.py").exists():
    _ROOT = _ROOT.parent

PATH = _ROOT / "01_src" / "00_common"
# ------------------------------------------------------------------------------------------


def _load_child(mod_name: str, file_path: Path):
    """
    Lädt file_path als Submodul src.common.<mod_name>.

    - registriert es in sys.modules
    - hängt es als Attribut an das Paket src.common
    """
    package_name = __name__            # "src.common"
    qualname = f"{package_name}.{mod_name}"  # z.B. "src.common.io_yaml"

    # Falls schon geladen, direkt zurückgeben
    if qualname in sys.modules:
        return sys.modules[qualname]

    spec = spec_from_file_location(qualname, str(file_path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Kann Spec für {qualname} aus {file_path} nicht erstellen")

    mod = module_from_spec(spec)
    sys.modules[qualname] = mod
    spec.loader.exec_module(mod)  # type: ignore[attr-defined]

    # Modul auch als Attribut im Paket registrieren:
    pkg = sys.modules.get(package_name)
    if pkg is not None:
        setattr(pkg, mod_name, mod)

    return mod


__all__: list[str] = []

# Alle .py-Dateien in 01_src/00_common automatisch laden
for pyfile in PATH.glob("*.py"):
    # __init__.py dort überspringen
    if pyfile.name == "__init__.py":
        continue

    mod_name = pyfile.stem  # Dateiname ohne .py
    try:
        _load_child(mod_name, pyfile)
        __all__.append(mod_name)
    except Exception as e:
        print(f"⚠️ Fehler beim Laden von src.common.{mod_name}: {e}")
        # Wenn du später „hart failen“ willst:
        # raise
