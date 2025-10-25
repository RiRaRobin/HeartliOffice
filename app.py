from __future__ import annotations
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

ROOT = Path(__file__).resolve().parent

def load_ui(path: Path):
    loader = QUiLoader()
    f = QFile(str(path))
    f.open(QFile.ReadOnly)
    try:
        ui = loader.load(f)
    finally:
        f.close()
    if ui is None:
        raise RuntimeError(f"Konnte UI nicht laden: {path}")
    return ui

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # .ui laden
        self.ui = load_ui(ROOT / "ui" / "main_window.ui")
        self.setCentralWidget(self.ui.centralWidget())

        # Widgets referenzieren
        self.table = self.ui.findChild(type(self.ui), "tableTasks")  # einfacher Trick, reicht fürs Testen
        # Spaltenköpfe setzen
        # headers = ["ID","Beschreibung","Projekt","Status","Prio","Fällig","in Tagen"]
        # self.table.setColumnCount(len(headers))
        # self.table.setHorizontalHeaderLabels(headers)

        # Testdaten (nur zum Sehen, dass alles steht)
        demo = [
            ["T-001","Schaltplan prüfen","ABC","OPEN","2","2025-11-05","12"],
            ["T-002","Stückliste erstellen","ABC","READY","3","2025-10-30","6"],
        ]
        # self.table.setRowCount(len(demo))
        # for i, row in enumerate(demo):
            # for j, val in enumerate(row):
                # self.table.setItem(i, j, QTableWidgetItem(val))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.setWindowTitle("Heartli OfficeTool")
    w.resize(1100, 700)
    w.show()
    sys.exit(app.exec())
