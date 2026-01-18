# make_folder_structure_md.py
# imports
import os
from pathlib import Path

# ============================================================
# ✅ USER SETTINGS (edit these paths directly in this file)
# ============================================================

# Input folder (can be anywhere, inside or outside your repo)
# INPUT_FOLDER = r"F:\Engineering\STASIG\02_ENG_ETCS\32_Projects\ETCS_CH_SBB Flirt Evo_L-4525_S-20019\06 STASIG Documents"  # e.g. r"D:\Projects\SomeFolder"
INPUT_FOLDER = r"F:\Engineering\STASIG\02_ENG_ETCS\32_Projects\ETCS_CH_SBB Flirt Evo_L-4525_S-20019\03 Suppliers Documents"  # e.g. r"D:\Projects\SomeFolder"

# Output files (full path incl. filename)
# OUTPUT_FOLDERS_ONLY_MD = r"C:\Users\robmue\Desktop\folder_structure.md"  # e.g. r"D:\out\folders_only.md"
# OUTPUT_WITH_FILES_MD = r"C:\Users\robmue\Desktop\folder_structure_with_files.md"  # e.g. r"D:\out\full_tree.md"

OUTPUT_FOLDERS_ONLY_MD = r"C:\Users\robmue\Desktop\folder_structure_supplier.md"  # e.g. r"D:\out\folders_only.md"
OUTPUT_WITH_FILES_MD = r"C:\Users\robmue\Desktop\folder_structure_with_files_supplier.md"  # e.g. r"D:\out\full_tree.md"

# Excluded folders (empty by default, as requested)
EXCLUDE_FOLDERS = set()  # e.g. {".git", ".venv", "__pycache__"}

# File extensions to exclude from file listing (case-insensitive)
EXCLUDE_FILE_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".bmp", ".dia", ".tiff", ".tif", ".gif", ".webp", ".svg", ".mp4", ".avi", ".mov", ".wav"
}

# ============================================================
# DISPLAY SETTINGS
# ============================================================
INDENT_SYMBOL = "│   "
BRANCH_SYMBOL = "├── "


def get_icon_for_file(filename: str) -> str:
    """Assign icons to file types, with a special rule for README."""
    lower = filename.lower()
    if lower == "readme.md":
        return "ℹ️"

    ext = os.path.splitext(filename)[1].lower()
    return {
        # Code & data
        ".py": "🐍",
        ".ipynb": "📓",
        ".csv": "📈",
        ".pkl": "🧠",
        ".json": "🧾",
        ".sqlite": "🗄️",
        ".db": "🗄️",

        # Text & docs
        ".md": "📄",
        ".txt": "📃",
        ".pdf": "📑",

        # Word
        ".doc": "📘",
        ".docx": "📘",
        ".dot": "📘",
        ".dotx": "📘",

        # Excel
        ".xls": "📊",
        ".xlsx": "📊",
        ".xlsm": "📊",
        ".xlsb": "📊",

        # PowerPoint
        ".ppt": "📽️",
        ".pptx": "📽️",
        ".pptm": "📽️",

        # Images
        ".png": "🖼️",
        ".jpg": "🖼️",
        ".jpeg": "🖼️",
        ".bmp": "🖼️",
        ".tiff": "🖼️",

    }.get(ext, "📄")

def should_list_file(filename: str) -> bool:
    """Return True if the file should be shown in output."""
    if filename.startswith("."):
        return False
    ext = Path(filename).suffix.lower()
    if ext in EXCLUDE_FILE_EXTENSIONS:
        return False
    return True


def write_structure(start_path: Path, folders_only_path: Path, full_path: Path) -> None:
    start_path = start_path.expanduser().resolve()
    folders_only_path = folders_only_path.expanduser().resolve()
    full_path = full_path.expanduser().resolve()

    if not start_path.exists():
        raise FileNotFoundError(f"Input path does not exist: {start_path}")
    if not start_path.is_dir():
        raise NotADirectoryError(f"Input path is not a directory: {start_path}")

    # ensure output folders exist
    folders_only_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.parent.mkdir(parents=True, exist_ok=True)

    base_name = start_path.name

    with folders_only_path.open("w", encoding="utf-8") as f1, full_path.open("w", encoding="utf-8") as f2:
        # Header
        f1.write("# 📁 Project Folder Structure (folders only)\n\n")
        f1.write("```text\n")
        f1.write(f"{base_name}/\n")

        f2.write("# 📁 Project Folder Structure (with files)\n\n")
        f2.write(
            "Legend:\n"
            "🐍 Python 📈 CSV 🧠 Pickle 📄 Markdown 📃 Text 🧾 JSON 🗄️ DB 🖼️ Image 📑 PDF 📓 Notebook ℹ️ README\n\n"
        )
        f2.write("```text\n")
        f2.write(f"{base_name}/\n")

        # Root files
        root_files = [
            p.name
            for p in sorted(start_path.iterdir(), key=lambda x: x.name.lower())
            if p.is_file() and should_list_file(p.name)
        ]
        for file in root_files:
            icon = get_icon_for_file(file)
            f2.write(f"{BRANCH_SYMBOL}{icon} {file}\n")

        last_top_level = None

        for root, dirs, files in os.walk(str(start_path)):
            # exclude dirs (if any set)
            if EXCLUDE_FOLDERS:
                dirs[:] = [d for d in dirs if d not in EXCLUDE_FOLDERS]

            # ignore hidden files
            files = [f for f in files if should_list_file(f)]

            rel_path = os.path.relpath(root, str(start_path))
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

            # Write folder
            f1.write(f"{indent}{current_folder}/\n")
            f2.write(f"{indent}{current_folder}/\n")

            # Files in folder
            sub_indent = INDENT_SYMBOL * level
            for file in sorted(files, key=str.lower):
                icon = get_icon_for_file(file)
                f2.write(f"{sub_indent}{icon} {file}\n")

        f1.write("```\n")
        f2.write("```\n")

    print(f"✅ Struktur gespeichert in: {folders_only_path}")
    print(f"📄 Struktur mit Dateien gespeichert in: {full_path}")


if __name__ == "__main__":
    write_structure(
        start_path=Path(INPUT_FOLDER),
        folders_only_path=Path(OUTPUT_FOLDERS_ONLY_MD),
        full_path=Path(OUTPUT_WITH_FILES_MD),
    )
