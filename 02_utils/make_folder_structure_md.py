# make_folder_structure_md.py
## import path_config.py
import sys
from pathlib import Path
current = Path(__file__).resolve()
project_root = current
while not (project_root / "path_config.py").exists() and project_root != project_root.parent:
    project_root = project_root.parent

sys.path.insert(0, str(project_root))
from path_config import convert_to_string, LEGACY

## regular imports
import os

# PATHS

# Folders that are to be ignored
EXCLUDE_FOLDERS = {".venv", ".git", "__pycache__", ".idea", ".vscode", ".mypy_cache", "venv"}

# Display symbols
INDENT_SYMBOL = "│   "
BRANCH_SYMBOL = "├── "

# Functions
def get_icon_for_file(filename):
    """Weise Dateitypen passende Emojis zu, mit Sonderregel für README"""
    lower = filename.lower()
    if lower == "readme.md":
        return "ℹ️"
    ext = os.path.splitext(filename)[1].lower()
    return {
        ".py": "🐍",
        ".csv": "📈",
        ".pkl": "🧠",
        ".md": "📄",
        ".txt": "📃",
        ".json": "🧾",
        ".sqlite": "🗄️",
        ".db": "🗄️",
        ".png": "🖼️",
        ".jpg": "🖼️",
        ".jpeg": "🖼️",
        ".pdf": "📑",
        ".ipynb": "📓"
    }.get(ext, "📄")

def is_condensed_folder(rel_path):
    """Bestimmt, ob ein Ordner komprimiert dargestellt werden soll"""
    rel_path_normalized = rel_path.replace("\\", "/")
    return (
        rel_path_normalized.startswith(convert_to_string(LEGACY))
    )

def write_structure(start_path, folders_only_path="folder_structure.md", full_path="folder_structure_with_files.md"):
    base_name = os.path.basename(os.path.abspath(start_path))

    with open(folders_only_path, "w", encoding="utf-8") as f1, open(full_path, "w", encoding="utf-8") as f2:
        # Header
        f1.write("# 📁 Project Folder Structure (folders only)\n\n")
        f1.write("```text\n")
        f1.write(f"{base_name}/\n")

        f2.write("# 📁 Project Folder Structure (with files)\n\n")
        f2.write("Legend:\n")
        f2.write("🐍 Python 📈 CSV 🧠 Pickle 📄 Markdown 📃 Text 🧾 JSON 🗄️ DB 🖼️ Image 📑 PDF 📓 Notebook ℹ️ README\n\n")
        f2.write("```text\n")
        f2.write(f"{base_name}/\n")

        # 🔹 Dateien im Root-Verzeichnis anzeigen
        root_files = [f for f in sorted(os.listdir(start_path)) if os.path.isfile(os.path.join(start_path, f)) and not f.startswith(".")]
        for file in root_files:
            icon = get_icon_for_file(file)
            f2.write(f"{BRANCH_SYMBOL}{icon} {file}\n")

        last_top_level = None

        for root, dirs, files in os.walk(start_path):
            # Filtere ignorierte Ordner und versteckte Dateien
            dirs[:] = [d for d in dirs if d not in EXCLUDE_FOLDERS]
            files = [f for f in files if not f.startswith(".")]

            rel_path = os.path.relpath(root, start_path)
            if rel_path == ".":
                continue

            parts = rel_path.split(os.sep)
            level = len(parts)
            indent = INDENT_SYMBOL * (level - 1) + BRANCH_SYMBOL
            current_folder = parts[-1]

            top_level = parts[0]
            if top_level != last_top_level:
                f1.write("\n")
                f2.write("\n")
                last_top_level = top_level

            # Ordner schreiben
            f1.write(f"{indent}{current_folder}/\n")
            f2.write(f"{indent}{current_folder}/\n")
            sub_indent = INDENT_SYMBOL * level

            # 📦 Komprimierte Anzeige für bestimmte Ordner
            if is_condensed_folder(rel_path) and len(files) > 2:
                files_by_ext = {}
                for file in sorted(files):
                    ext = os.path.splitext(file)[1].lower()
                    files_by_ext.setdefault(ext, []).append(file)

                for ext, file_list in files_by_ext.items():
                    if len(file_list) <= 2:
                        for f in file_list:
                            icon = get_icon_for_file(f)
                            f2.write(f"{sub_indent}{icon} {f}\n")
                    else:
                        first = file_list[0]
                        last = file_list[-1]
                        icon = get_icon_for_file(first)
                        f2.write(f"{sub_indent}{icon} {first}\n")
                        f2.write(f"{sub_indent}… ({len(file_list)-2} more {ext or 'files'})\n")
                        f2.write(f"{sub_indent}{icon} {last}\n")
            else:
                # 🧾 Normale Dateiauflistung für alle anderen Ordner
                for file in sorted(files):
                    icon = get_icon_for_file(file)
                    f2.write(f"{sub_indent}{icon} {file}\n")

        f1.write("```\n")
        f2.write("```\n")

    print(f"✅ Struktur gespeichert in '{folders_only_path}'")
    print(f"📄 Struktur mit Dateien gespeichert in '{full_path}'")

# main
if __name__ == "__main__":
    PROJECT_ROOT = os.path.abspath(".")
    write_structure(PROJECT_ROOT)
