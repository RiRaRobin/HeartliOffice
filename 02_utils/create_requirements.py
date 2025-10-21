# create_requirements.py
## import path_config.py
import sys
from pathlib import Path
current = Path(__file__).resolve()
project_root = current
while not (project_root / "path_config.py").exists() and project_root != project_root.parent:
    project_root = project_root.parent

sys.path.insert(0, str(project_root))
from path_config import convert_to_string, CODE

## regular imports
import os
import re
import sys
import importlib.metadata as metadata

## PATHS
PY_FOLDER = convert_to_string(CODE)
OUTPUT_FILE = "requirements.txt"

## GLOBALS
BUILTIN_MODULES = set(sys.builtin_module_names) | {
    "os", "sys", "re", "math", "time", "datetime", "json",
    "itertools", "collections", "pathlib", "typing", "statistics",
    "functools", "copy", "pprint", "string", "subprocess", "threading",
    "unittest", "warnings", "logging", "argparse", "enum", "traceback",
    "importlib"
}

# Functions
def extract_imports_from_py(folder):
    imports = set()
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".py"):
                with open(os.path.join(root, file), encoding="utf-8") as f:
                    for line in f:
                        match = re.match(r"^\s*(import|from)\s+([\w\.]+)", line)
                        if match:
                            pkg = match.group(2).split(".")[0]
                            if pkg not in BUILTIN_MODULES and pkg != "path_config":
                                imports.add(pkg)
    return sorted(imports)

def get_installed_versions(packages):
    result = {}
    for pkg in packages:
        try:
            version = metadata.version(pkg)
            result[pkg] = version
        except metadata.PackageNotFoundError:
            print(f"⚠️ Package '{pkg}' not found in current environment.")
        except Exception as e:
            print(f"⚠️ Error checking '{pkg}': {e}")
    return result

def write_requirements(pkg_versions, path):
    with open(path, "w", encoding="utf-8") as f:
        for pkg, version in sorted(pkg_versions.items()):
            f.write(f"{pkg}=={version}\n")

# main
if __name__ == "__main__":
    print("🔍 Scanning Python files for imports...")
    packages = extract_imports_from_py(PY_FOLDER)
    print(f"📦 Found {len(packages)} external packages")

    print("📋 Resolving package versions...")
    pkg_versions = get_installed_versions(packages)

    print(f"💾 Writing to {OUTPUT_FILE}...")
    write_requirements(pkg_versions, OUTPUT_FILE)

    print("✅ Done.")
