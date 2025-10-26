# 01_src/03_questions/question_dialog.py
from __future__ import annotations

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

from src.questions.questions_service import ( # type: ignore
    save_new_question, load_questions_active, TYPES,
    update_question,
)

class QuestionDialog(QDialog):
    def __init__(self, parent=None, mode: str = "create", question: dict | None = None):
        super().__init__(parent)
        self.mode = mode
        self.edit_id = (question or {}).get("id")
        self.created_id: str | None = None

        self.setWindowTitle("Neue Frage" if self.mode == "create" else "Frage bearbeiten")

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

        # Prefill im Edit-Modus
        if self.mode == "edit" and question:
            person = (question.get("person") or "").strip()
            if person and person not in persons:
                self.cbPerson.addItem(person)
            self.cbPerson.setCurrentText(person)
            self.teFrage.setPlainText(question.get("frage",""))
            self.cbTyp.setCurrentText(question.get("typ","FRAGE"))
            self.leLinkedTask.setText(question.get("linked_task_id",""))
            self.teNotes.setPlainText(question.get("notes",""))

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

        if self.mode == "edit" and self.edit_id:
            update_question(self.edit_id, {
                "person": person, "frage": frage, "typ": typ,
                "linked_task_id": linked, "notes": notes,
            })
            self.created_id = self.edit_id
        else:
            self.created_id = save_new_question({
                "person": person, "frage": frage, "typ": typ,
                "linked_task_id": linked, "notes": notes,
            })
        self.accept()
