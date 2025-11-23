"""
src.questions
Alias-Loader für alle Module im Ordner 01_src/03_questions.

Erlaubt z.B.:
    from src.questions.questions_service import load_questions_active
"""

from __future__ import annotations

import sys
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path

# --- Projekt-ROOT anhand path_config.py finden ---
_THIS = Path(__file__).resolve()
_ROOT = _THIS
while _ROOT != _ROOT.parent and not (_ROOT / "path_config.py").exists():
    _ROOT = _ROOT.parent

# ROOT in sys.path eintragen, damit 'path_config' importierbar ist
root_str = str(_ROOT)
if root_str not in sys.path:
    sys.path.insert(0, root_str)

CODE_QUESTIONS = _ROOT / "01_src" / "03_questions"
# -------------------------------------------------


def _load_child(mod_name: str, file_path: Path):
    """
    Lädt file_path als Submodul src.questions.<mod_name>.

    - registriert es in sys.modules
    - hängt es als Attribut an das Paket src.questions
    """
    package_name = __name__                 # "src.questions"
    qualname = f"{package_name}.{mod_name}" # z.B. "src.questions.questions_service"

    # schon geladen?
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

# Alle .py-Dateien in 01_src/03_questions automatisch laden
for pyfile in CODE_QUESTIONS.glob("*.py"):
    if pyfile.name == "__init__.py":
        continue

    mod_name = pyfile.stem  # Dateiname ohne .py
    try:
        _load_child(mod_name, pyfile)
        __all__.append(mod_name)
    except Exception as e:
        print(f"⚠️ Fehler beim Laden von {__name__}.{mod_name}: {e}")
        # optional streng:
        # raise
