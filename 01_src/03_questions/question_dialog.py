# 01_src/03_questions/question_dialog.py
from __future__ import annotations

# Bootstrap ROOT → sys.path und src-Alias
import sys
from pathlib import Path

_CUR = Path(__file__).resolve()
_ROOT = _CUR
while _ROOT != _ROOT.parent and not (_ROOT / "path_config.py").exists():
    _ROOT = _ROOT.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
import src  # noqa: F401

from PySide6.QtWidgets import (
    QDialog, QDialogButtonBox, QVBoxLayout, QFormLayout,
    QComboBox, QTextEdit, QLineEdit
)

from src.questions.questions_service import save_new_question, load_questions_active, TYPES # type: ignore

class QuestionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Neue Frage")

        # Layouts
        root = QVBoxLayout(self)
        form = QFormLayout()
        root.addLayout(form)

        # Widgets
        self.cbPerson = QComboBox()
        self.cbPerson.setEditable(True)
        persons = sorted({ (q.get("person") or "").strip()
                           for q in load_questions_active()
                           if (q.get("person") or "").strip() })
        self.cbPerson.addItems(persons)

        self.teFrage = QTextEdit()
        self.teFrage.setMinimumHeight(100)

        self.cbTyp = QComboBox()
        self.cbTyp.addItems(TYPES)

        self.leLinkedTask = QLineEdit()
        self.teNotes = QTextEdit()
        self.teNotes.setMinimumHeight(60)

        form.addRow("Person", self.cbPerson)
        form.addRow("Frage", self.teFrage)
        form.addRow("Typ", self.cbTyp)
        form.addRow("Verlinkter Task (optional)", self.leLinkedTask)
        form.addRow("Notizen", self.teNotes)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        root.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.on_save)
        self.buttonBox.rejected.connect(self.reject)

        self.created_id: str | None = None

    def on_save(self):
        person = (self.cbPerson.currentText() or "").strip()
        frage  = (self.teFrage.toPlainText() or "").strip()
        typ    = (self.cbTyp.currentText() or "FRAGE").strip()
        linked = (self.leLinkedTask.text() or "").strip()
        notes  = (self.teNotes.toPlainText() or "").strip()

        if not person or not frage:
            if not person: self.cbPerson.setFocus()
            elif not frage: self.teFrage.setFocus()
            return

        self.created_id = save_new_question({
            "person": person,
            "frage": frage,
            "typ": typ,
            "linked_task_id": linked,
            "notes": notes,
        })
        self.accept()
