# 01_src/01_tasks/task_dialog.py
from __future__ import annotations

# --- Bootstrap: Projekt-ROOT & Alias-Package 'src' aktivieren
import sys
from pathlib import Path

_CUR = Path(__file__).resolve()
_ROOT = _CUR
while _ROOT != _ROOT.parent and not (_ROOT / "path_config.py").exists():
    _ROOT = _ROOT.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
import src  # noqa: F401

# --- Qt & Services
from PySide6.QtWidgets import (
    QDialog, QLineEdit, QTextEdit, QComboBox, QSpinBox, QDateEdit,
    QDialogButtonBox, QVBoxLayout
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QDate

from src.tasks.tasks_service import save_new_task, STATUS_VALUES, PRIO_VALUES  # type: ignore


class TaskDialog(QDialog):
    """Dialog zum Erfassen einer neuen Aufgabe. Nach accept(): self.created_id enthält die neue ID."""
    def __init__(self, parent=None):
        super().__init__(parent)

        # UI laden (du hast task_dialog.ui direkt in 01_src/01_tasks/ abgelegt)
        ui_path = _ROOT / "01_src" / "01_tasks" / "task_dialog.ui"
        loader = QUiLoader()
        f = QFile(str(ui_path))
        if not f.open(QFile.ReadOnly):
            raise RuntimeError(f"Kann UI nicht öffnen: {ui_path}")
        try:
            self._root = loader.load(f, None)   # Top-Level-Widget aus .ui
        finally:
            f.close()
        if self._root is None:
            raise RuntimeError("Konnte task_dialog.ui nicht laden")

        # Geladenes UI in diesen QDialog einbetten → sichtbar machen
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self._root)

        self.setWindowTitle("Neue Aufgabe")
        self.created_id: str | None = None

        # Widgets vom geladenen Root holen (Namen müssen mit objectName im Designer übereinstimmen)
        self.leProjekt: QLineEdit        = self._root.findChild(QLineEdit, "leProjekt")
        self.teBeschreibung: QTextEdit   = self._root.findChild(QTextEdit, "teBeschreibung")
        self.leDokNr: QLineEdit          = self._root.findChild(QLineEdit, "leDokNr")
        self.leDokName: QLineEdit        = self._root.findChild(QLineEdit, "leDokName")
        self.deAuftrag: QDateEdit        = self._root.findChild(QDateEdit, "deAuftrag")
        self.deFaellig: QDateEdit        = self._root.findChild(QDateEdit, "deFaellig")
        self.cbStatus: QComboBox         = self._root.findChild(QComboBox, "cbStatus")
        self.sbPrio: QSpinBox            = self._root.findChild(QSpinBox, "sbPrio")
        self.teNotizen: QTextEdit        = self._root.findChild(QTextEdit, "teNotizen")
        self.teFollow: QTextEdit         = self._root.findChild(QTextEdit, "teFollow")
        self.buttonBox: QDialogButtonBox = self._root.findChild(QDialogButtonBox, "buttonBox")

        # Sanity-Check: wenn ein zentrales Widget None ist, früh scheitern (hilft beim Debugging der objectNames)
        for name, w in {
            "teBeschreibung": self.teBeschreibung,
            "cbStatus": self.cbStatus,
            "sbPrio": self.sbPrio,
            "buttonBox": self.buttonBox,
        }.items():
            if w is None:
                raise RuntimeError(f"Widget '{name}' nicht im UI gefunden (objectName prüfen).")

        # Defaults
        if self.deAuftrag is not None:
            self.deAuftrag.setDate(QDate.currentDate())
        if self.deFaellig is not None:
            tomorrow = QDate.currentDate().addDays(1)
            self.deFaellig.setDate(tomorrow)
        if self.cbStatus is not None:
            self.cbStatus.addItems(STATUS_VALUES)
        if self.sbPrio is not None:
            self.sbPrio.setRange(min(PRIO_VALUES), max(PRIO_VALUES))
            self.sbPrio.setValue(2)

        # Signals
        self.buttonBox.accepted.connect(self.on_save)
        self.buttonBox.rejected.connect(self.reject)
        if self.leProjekt is not None:
            self.leProjekt.setFocus()

    # ----------------------------
    # Slot: Speichern gedrückt
    # ----------------------------
    def on_save(self) -> None:
        """Liest die Felder aus, speichert via save_new_task und schließt mit accept()."""
        beschr = (self.teBeschreibung.toPlainText() if self.teBeschreibung else "").strip()
        if not beschr:
            # Minimal-Validierung: Beschreibung ist Pflicht
            if self.teBeschreibung:
                self.teBeschreibung.setFocus()
            return

        data = {
            "beschreibung": beschr,
            "projekt": (self.leProjekt.text() if self.leProjekt else "").strip(),
            "dokument_nr": (self.leDokNr.text() if self.leDokNr else "").strip(),
            "dokument_name": (self.leDokName.text() if self.leDokName else "").strip(),
            "auftrag_erhalten": self.deAuftrag.date().toString("yyyy-MM-dd") if self.deAuftrag else "",
            "faellig_bis": self.deFaellig.date().toString("yyyy-MM-dd") if self.deFaellig and self.deFaellig.date().isValid() else "",
            "status": self.cbStatus.currentText() if self.cbStatus else "OPEN",
            "dringlichkeit": int(self.sbPrio.value()) if self.sbPrio else 2,
            "notizen": self.teNotizen.toPlainText() if self.teNotizen else "",
            "follow_up": self.teFollow.toPlainText() if self.teFollow else "",
        }

        tid = save_new_task(data)
        self.created_id = tid
        self.accept()
