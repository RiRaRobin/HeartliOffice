# 01_src/04_files/file_dialog.py
from __future__ import annotations

# --- Bootstrap: Projekt-ROOT & src-Alias ---
import sys
from pathlib import Path
from typing import Dict, Any, List

_CUR = Path(__file__).resolve()
_ROOT = _CUR
while _ROOT != _ROOT.parent and not (_ROOT / "path_config.py").exists():
    _ROOT = _ROOT.parent

if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import src  # noqa: F401

# --- Qt & Services ---
from PySide6.QtWidgets import (
    QDialog, QLineEdit, QTextEdit, QComboBox,
    QDialogButtonBox, QVBoxLayout, QPushButton,
    QListWidget, QListWidgetItem, QCompleter
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt

from src.files.files_service import (  # type: ignore
    save_new_file, save_existing_file, load_files_active,
)


def _extract_id(label: str) -> str:
    """
    Nimmt einen Label-String wie
        'F-xxx | BU-xxx | Name'
    und gibt nur die ID zurück ('F-xxx').
    Falls kein '|' enthalten ist, wird der Text direkt zurückgegeben.
    """
    s = label.strip()
    if not s:
        return ""
    if "|" in s:
        return s.split("|", 1)[0].strip()
    return s


class FileDialog(QDialog):
    """
    Dialog zum Erstellen oder Bearbeiten eines Files.

    mode: "create" | "edit"
    file_data: Dict mit Feldern wie im YAML (nur für edit)
    """

    def __init__(self, parent=None, mode: str = "create", file_data: Dict[str, Any] | None = None):
        super().__init__(parent)
        self.mode = mode
        self.edit_id: str | None = (file_data or {}).get("id")
        self.created_id: str | None = None

        # --- UI laden ---
        ui_path = _ROOT / "01_src" / "04_files" / "file_dialog.ui"
        loader = QUiLoader()
        f = QFile(str(ui_path))
        if not f.open(QFile.ReadOnly):
            raise RuntimeError(f"Kann UI nicht öffnen: {ui_path}")
        try:
            root = loader.load(f, None)
        finally:
            f.close()
        if root is None:
            raise RuntimeError("Konnte file_dialog.ui nicht laden")

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(root)

        self.setWindowTitle("Neues File" if self.mode == "create" else "File bearbeiten")

        # --- Widgets aus .ui binden (Namen müssen zum Designer passen!) ---
        self.leProjekt: QLineEdit | None = root.findChild(QLineEdit, "leFileProject")
        self.cbTyp: QComboBox | None = root.findChild(QComboBox, "cbFileType")
        self.leRef: QLineEdit | None = root.findChild(QLineEdit, "leFileRef")
        self.leName: QLineEdit | None = root.findChild(QLineEdit, "leFileName")

        self.teBeschreibung: QTextEdit | None = root.findChild(QTextEdit, "teFileDescription")
        self.teNotizen: QTextEdit | None = root.findChild(QTextEdit, "teFileNotes")
        self.leTags: QLineEdit | None = root.findChild(QLineEdit, "leFileTags")

        # Links IN
        self.leLinksInInput: QLineEdit | None = root.findChild(QLineEdit, "leLinksInInput")
        self.btnAddLinkIn: QPushButton | None = root.findChild(QPushButton, "btnAddLinkIn")
        self.btnRemoveLinkIn: QPushButton | None = root.findChild(QPushButton, "btnRemoveLinkIn")
        self.listLinksIn: QListWidget | None = root.findChild(QListWidget, "listFileLinksIn")

        # Links OUT
        self.leLinksOutInput: QLineEdit | None = root.findChild(QLineEdit, "leLinksOutInput")
        self.btnAddLinkOut: QPushButton | None = root.findChild(QPushButton, "btnAddLinkOut")
        self.btnRemoveLinkOut: QPushButton | None = root.findChild(QPushButton, "btnRemoveLinkOut")
        self.listLinksOut: QListWidget | None = root.findChild(QListWidget, "listFileLinksOut")

        self.buttonBox: QDialogButtonBox | None = root.findChild(QDialogButtonBox, "buttonBox")

        # Minimal-Checks für kritische Widgets
        for name, w in {
            "leFileName": self.leName,
            "cbFileType": self.cbTyp,
            "buttonBox": self.buttonBox,
        }.items():
            if w is None:
                raise RuntimeError(f"Widget '{name}' nicht im UI gefunden (objectName im Designer prüfen).")

        # --- Typ-Auswahl füllen ---
        if self.cbTyp is not None:
            self.cbTyp.clear()
            self.cbTyp.addItems(["BU", "PFAD"])

        # --- QCompleter für Links IN / OUT ---
        choices: List[str] = []
        try:
            rows = load_files_active()
            for r in rows:
                fid = str(r.get("id", "")).strip()
                ref = str(r.get("ref", "")).strip()
                name = str(r.get("name", "")).strip()
                parts = [fid] if fid else []
                if ref:
                    parts.append(ref)
                if name:
                    parts.append(name)
                label = " | ".join(parts)
                if label:
                    choices.append(label)
        except Exception:
            choices = []

        if choices:
            comp_in = QCompleter(choices, self)
            comp_in.setCaseSensitivity(Qt.CaseInsensitive)
            comp_in.setFilterMode(Qt.MatchContains)

            comp_out = QCompleter(choices, self)
            comp_out.setCaseSensitivity(Qt.CaseInsensitive)
            comp_out.setFilterMode(Qt.MatchContains)

            if self.leLinksInInput:
                self.leLinksInInput.setCompleter(comp_in)
            if self.leLinksOutInput:
                self.leLinksOutInput.setCompleter(comp_out)

        # --- Buttons für Links verdrahten ---
        if self.btnAddLinkIn and self.leLinksInInput and self.listLinksIn:
            self.btnAddLinkIn.clicked.connect(
                lambda: self._add_link_from_input(self.leLinksInInput, self.listLinksIn)
            )
        if self.btnRemoveLinkIn and self.listLinksIn:
            self.btnRemoveLinkIn.clicked.connect(
                lambda: self._remove_selected(self.listLinksIn)
            )

        if self.btnAddLinkOut and self.leLinksOutInput and self.listLinksOut:
            self.btnAddLinkOut.clicked.connect(
                lambda: self._add_link_from_input(self.leLinksOutInput, self.listLinksOut)
            )
        if self.btnRemoveLinkOut and self.listLinksOut:
            self.btnRemoveLinkOut.clicked.connect(
                lambda: self._remove_selected(self.listLinksOut)
            )

        # --- Prefill im Edit-Modus ---
        if self.mode == "edit" and file_data:
            if self.leProjekt:
                self.leProjekt.setText(file_data.get("projekt", ""))
            if self.leRef:
                self.leRef.setText(file_data.get("ref", ""))
            if self.leName:
                self.leName.setText(file_data.get("name", ""))
            if self.teBeschreibung:
                self.teBeschreibung.setPlainText(file_data.get("beschreibung", ""))
            if self.teNotizen:
                self.teNotizen.setPlainText(file_data.get("notizen", ""))

            # Tags
            tags = file_data.get("tags") or []
            if isinstance(tags, list):
                tags_str = ", ".join(str(t) for t in tags)
            else:
                tags_str = str(tags)
            if self.leTags:
                self.leTags.setText(tags_str)

            # Links IN / OUT
            links_in = file_data.get("links_in") or []
            links_out = file_data.get("links_out") or []

            if self.listLinksIn:
                self.listLinksIn.clear()
                for x in links_in:
                    self.listLinksIn.addItem(str(x))

            if self.listLinksOut:
                self.listLinksOut.clear()
                for x in links_out:
                    self.listLinksOut.addItem(str(x))

            # Typ
            if self.cbTyp:
                cur_typ = file_data.get("typ", "BU")
                idx = self.cbTyp.findText(cur_typ)
                self.cbTyp.setCurrentIndex(max(idx, 0))

        # --- ButtonBox ---
        if self.buttonBox:
            self.buttonBox.accepted.connect(self.on_save)
            self.buttonBox.rejected.connect(self.reject)

        if self.leName:
            self.leName.setFocus()

    # -------------------------------------------------
    # Hilfsfunktionen für Links-Listen
    # -------------------------------------------------
    def _add_link_from_input(self, line: QLineEdit, lst: QListWidget) -> None:
        raw = line.text().strip()
        if not raw:
            return

        ident = _extract_id(raw)
        if not ident:
            line.clear()
            return

        # Duplikate vermeiden
        for i in range(lst.count()):
            if lst.item(i).text().strip() == ident:
                line.clear()
                return

        lst.addItem(ident)
        line.clear()

    def _remove_selected(self, lst: QListWidget) -> None:
        for item in lst.selectedItems():
            row = lst.row(item)
            lst.takeItem(row)

    # -------------------------------------------------
    # Speichern
    # -------------------------------------------------
    def on_save(self) -> None:
        name = (self.leName.text() if self.leName else "").strip()
        if not name:
            if self.leName:
                self.leName.setFocus()
            return

        # Tags (Komma-getrennt)
        tags: List[str] = []
        if self.leTags:
            raw = self.leTags.text().strip()
            if raw:
                tags = [t.strip() for t in raw.split(",") if t.strip()]

        # Links aus den Listen einsammeln
        def collect_links(lst: QListWidget | None) -> List[str]:
            out: List[str] = []
            if not lst:
                return out
            for i in range(lst.count()):
                txt = lst.item(i).text().strip()
                if txt:
                    out.append(txt)
            return out

        links_in = collect_links(self.listLinksIn)
        links_out = collect_links(self.listLinksOut)

        data = {
            "projekt": self.leProjekt.text().strip() if self.leProjekt else "",
            "typ": self.cbTyp.currentText() if self.cbTyp else "BU",
            "ref": self.leRef.text().strip() if self.leRef else "",
            "name": name,
            "beschreibung": self.teBeschreibung.toPlainText().strip() if self.teBeschreibung else "",
            "tags": tags,
            "notizen": self.teNotizen.toPlainText().strip() if self.teNotizen else "",
            "links_in": links_in,
            "links_out": links_out,
        }

        if self.mode == "edit" and self.edit_id:
            file_id = save_existing_file(self.edit_id, data)
        else:
            file_id = save_new_file(data)

        self.created_id = file_id
        self.accept()
