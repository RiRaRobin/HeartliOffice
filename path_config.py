# path_config.py
from pathlib import Path

# === Basis: Automatically recognise project root ===
ROOT = Path(__file__).resolve().parent



# === Data structure ===
DATA = Path("00_data")
DATA_EXAMPLES = DATA / "00_examples"

DATA_TASKS = DATA / "01_tasks"

DATA_MEETINGS = DATA / "02_meetings"

DATA_QUESTIONS = DATA / "03_questions"


# === Code ===
CODE = Path("01_src")
CODE_TASKS = CODE / "01_tasks"

CODE_MEETINGS = CODE / "02_meetings"

CODE_QUESTIONS = CODE / "03_questions"



# === Utils ===
UTILS = Path("02_utils")



# === Legacy ===
LEGACY = Path("03_legacy")






# === Setup-Funktion zum Anlegen aller benötigten Ordner ===
def create_all_directories():
    all_paths = [v for k, v in globals().items() if isinstance(v, Path)]
    created = 0
    for path in all_paths:
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            created += 1
    print(f"✅ {created} Ordner wurden erstellt (falls nicht vorhanden).")

# === Prüffunktion zum Auflisten fehlender Pfade ===
def check_paths(verbose=True):
    for name, path in globals().items():
        if isinstance(path, Path) and not path.exists():
            if verbose:
                print(f"⚠️  {name} → Pfad existiert nicht: {path}")

# Helping Function for create requirements          
def convert_to_string(NAME):
    return str(NAME).replace("\\", ("/"))

# === Optional: direkt ausführbar als Tool ===
if __name__ == "__main__":
    print("🔍 Starte Pfadüberprüfung und Setup...")
    check_paths()
    create_all_directories()
