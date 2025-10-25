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
from PySide6.QtCore import QFile, QDate  # QDate GLOBAL importieren!

from src.tasks.tasks_service import ( # type: ignore
    save_new_task, save_existing_task, STATUS_VALUES, PRIO_VALUES
)  # type: ignore
from datetime import datetime

def _set_qdate_from_str(w: QDateEdit | None, s: str | None) -> None:
    """Setzt ein QDateEdit robust aus 'YYYY-MM-DD' oder ISO-String; setzt NICHT auf heute, wenn leer/unparsebar."""
    if not w:
        return
    s = (s or "").strip()
    if not s:
        return  # nichts setzen
    qd = QDate.fromString(s, "yyyy-MM-dd")
    if qd.isValid():
        w.setDate(qd); return
    try:
        d = datetime.fromisoformat(s).date()
        w.setDate(QDate(d.year, d.month, d.day))
    except Exception:
        pass  # nichts setzen, wichtiger als stillschweigend Defaults

class TaskDialog(QDialog):
    """Dialog zum Erfassen oder Bearbeiten einer Aufgabe.
       mode: "create" | "edit"
       task: dict mit Feldern wie in YAML (nur für edit)
    """
    def __init__(self, parent=None, mode: str = "create", task: dict | None = None):
        super().__init__(parent)
        self.mode = mode
        self.edit_id: str | None = (task or {}).get("id")
        self.created_id: str | None = None

        # --- UI laden (du hast task_dialog.ui direkt im Ordner 01_src/01_tasks/)
        ui_path = _ROOT / "01_src" / "01_tasks" / "task_dialog.ui"
        loader = QUiLoader()
        f = QFile(str(ui_path))
        if not f.open(QFile.ReadOnly):
            raise RuntimeError(f"Kann UI nicht öffnen: {ui_path}")
        try:
            root = loader.load(f, None)  # Top-Level-Widget aus .ui
        finally:
            f.close()
        if root is None:
            raise RuntimeError("Konnte task_dialog.ui nicht laden")

        # In diesen QDialog einbetten → sichtbar
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(root)

        self.setWindowTitle("Neue Aufgabe" if self.mode == "create" else "Aufgabe bearbeiten")

        # Widgets binden (objectName muss zum .ui passen)
        self.leProjekt: QLineEdit        = root.findChild(QLineEdit,   "leProjekt")
        self.teBeschreibung: QTextEdit   = root.findChild(QTextEdit,   "teBeschreibung")
        self.leDokNr: QLineEdit          = root.findChild(QLineEdit,   "leDokNr")
        self.leDokName: QLineEdit        = root.findChild(QLineEdit,   "leDokName")
        self.deAuftrag: QDateEdit        = root.findChild(QDateEdit,   "deAuftrag")
        self.deFaellig: QDateEdit        = root.findChild(QDateEdit,   "deFaellig")
        self.cbStatus: QComboBox         = root.findChild(QComboBox,   "cbStatus")
        self.sbPrio: QSpinBox            = root.findChild(QSpinBox,    "sbPrio")
        self.teNotizen: QTextEdit        = root.findChild(QTextEdit,   "teNotizen")
        self.teFollow: QTextEdit         = root.findChild(QTextEdit,   "teFollow")
        self.buttonBox: QDialogButtonBox = root.findChild(QDialogButtonBox, "buttonBox")

        # Minimal-Checks (hilft, falls objectNames im .ui anders sind)
        for name, w in {
            "teBeschreibung": self.teBeschreibung,
            "cbStatus": self.cbStatus,
            "sbPrio": self.sbPrio,
            "buttonBox": self.buttonBox,
        }.items():
            if w is None:
                raise RuntimeError(f"Widget '{name}' nicht im UI gefunden (objectName im .ui prüfen).")

        # --- Defaults (Create) oder Prefill (Edit)
        if self.mode == "edit" and task:
            # Strings
            if self.leProjekt:      self.leProjekt.setText(task.get("projekt",""))
            if self.teBeschreibung: self.teBeschreibung.setPlainText(task.get("beschreibung",""))
            if self.leDokNr:        self.leDokNr.setText(task.get("dokument_nr",""))
            if self.leDokName:      self.leDokName.setText(task.get("dokument_name",""))
            if self.teNotizen:      self.teNotizen.setPlainText(task.get("notizen",""))
            if self.teFollow:       self.teFollow.setPlainText(task.get("follow_up",""))

            # Status/Prio
            if self.cbStatus:
                self.cbStatus.clear()
                self.cbStatus.addItems(STATUS_VALUES)
                cur = task.get("status","OPEN")
                idx = self.cbStatus.findText(cur)
                self.cbStatus.setCurrentIndex(max(idx, 0))
            if self.sbPrio:
                self.sbPrio.setRange(min(PRIO_VALUES), max(PRIO_VALUES))
                try:
                    self.sbPrio.setValue(int(task.get("dringlichkeit", 2)))
                except Exception:
                    self.sbPrio.setValue(2)

            # 🚫 WICHTIG: hier KEINE Defaults setzen
            # Dates exakt aus YAML:
            _set_qdate_from_str(self.deAuftrag, task.get("auftrag_erhalten"))
            _set_qdate_from_str(self.deFaellig, task.get("faellig_bis"))

        else:
            # CREATE-Modus: hier dürfen Defaults gesetzt werden
            if self.deAuftrag is not None:
                self.deAuftrag.setDate(QDate.currentDate())
            if self.deFaellig is not None:
                self.deFaellig.setDate(QDate.currentDate().addDays(1))
            if self.cbStatus is not None:
                self.cbStatus.clear()
                self.cbStatus.addItems(STATUS_VALUES)
            if self.sbPrio is not None:
                self.sbPrio.setRange(min(PRIO_VALUES), max(PRIO_VALUES))
                self.sbPrio.setValue(2)

        # Signals
        self.buttonBox.accepted.connect(self.on_save)
        self.buttonBox.rejected.connect(self.reject)

        # Fokus
        if self.leProjekt:
            self.leProjekt.setFocus()

    # ----------------------------
    # Slot: Speichern gedrückt
    # ----------------------------
    def on_save(self) -> None:
        beschr = (self.teBeschreibung.toPlainText() if self.teBeschreibung else "").strip()
        if not beschr:
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

        if self.mode == "edit" and self.edit_id:
            tid = save_existing_task(self.edit_id, data)
        else:
            tid = save_new_task(data)

        self.created_id = tid
        self.accept()
