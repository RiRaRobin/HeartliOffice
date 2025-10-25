from __future__ import annotations
import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QPushButton, QSplitter,
    QHeaderView, QWidget, QLabel
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt
from PySide6.QtWidgets import QHeaderView, QTableWidget, QMessageBox, QTableWidgetItem
from src.tasks.task_dialog import TaskDialog # type: ignore
from src.tasks.tasks_service import load_tasks_active # type: ignore

ROOT = Path(__file__).resolve().parent
UI_FILE = ROOT / "ui" / "main_window.ui"


def load_ui(path: Path):
    loader = QUiLoader()
    f = QFile(str(path))
    if not f.open(QFile.ReadOnly):
        raise RuntimeError(f"Kann UI nicht öffnen: {path}")
    try:
        ui = loader.load(f)
    finally:
        f.close()
    if ui is None:
        raise RuntimeError(f"Kann UI nicht laden: {path}")
    return ui


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # --- UI laden ---
        loaded = load_ui(UI_FILE)
        self.setCentralWidget(loaded.centralwidget)

        self.root: QWidget = self.centralWidget()  # <— Root-Widget merken
        self.btnTaskNew = self.root.findChild(QPushButton, "btnTaskNew")
        if self.btnTaskNew:
            self.btnTaskNew.clicked.connect(self.on_task_new)


        # Splitter konfigurieren usw.
        splitter: QSplitter = self.root.findChild(QSplitter, "body_splitter")
        if splitter:
            splitter.setStretchFactor(0, 0)
            splitter.setStretchFactor(1, 1)

        # Header & Stack
        self.lblTitle: QLabel = self.root.findChild(QLabel, "lblTitle")
        self.stack: QStackedWidget = self.root.findChild(QStackedWidget, "mainStack")

        # Seiten
        self.pageHome: QWidget      = self.root.findChild(QWidget, "pageHome")
        self.pageTasks: QWidget     = self.root.findChild(QWidget, "pageTasks")
        self.pageMeetings: QWidget  = self.root.findChild(QWidget, "pageMeetings")
        self.pageQuestions: QWidget = self.root.findChild(QWidget, "pageQuestions")

        # Sidebar-Buttons
        self.btnHome: QPushButton      = self.root.findChild(QPushButton, "btnNavHome")
        self.btnTasks: QPushButton     = self.root.findChild(QPushButton, "btnNavTasks")
        self.btnMeetings: QPushButton  = self.root.findChild(QPushButton, "btnNavMeetings")
        self.btnQuestions: QPushButton = self.root.findChild(QPushButton, "btnNavQuestions")

        # Clicks verdrahten
        if self.btnHome:      self.btnHome.clicked.connect(lambda: self.show_page("Home"))
        if self.btnTasks:     self.btnTasks.clicked.connect(lambda: self.show_page("Tasks"))
        if self.btnMeetings:  self.btnMeetings.clicked.connect(lambda: self.show_page("Meetings"))
        if self.btnQuestions: self.btnQuestions.clicked.connect(lambda: self.show_page("Questions"))

        # Tabellen-Setup optional
        self.setup_tables()

        # Aktiven Button optisch markieren (optional)
        self.setStyleSheet("""
            QPushButton[active="true"] { background: #1f2937; color: #e5e7eb; border-radius: 8px; }
            QPushButton:hover { background: #111827; }
        """)
        
        self.show_page("Home")
        self.reload_tasks_views()


    # ----------------------------------------------------------
    #   Alle Tasks in Tabelle anzeigen
    # ----------------------------------------------------------
    def reload_tasks_views(self):
        """Füllt die Tasks-Tabelle neu (Alle Tasks)."""
        table = self.root.findChild(QTableWidget, "tableAllTasks")
        if not table:
            return

        rows = load_tasks_active()

        # Spalten: 0 ID | 1 Beschreibung | 2 Projekt | 3 Status | 4 Prio | 5 Fällig
        table.setSortingEnabled(False)
        table.clearContents()
        table.setRowCount(len(rows))

        for r, t in enumerate(rows):
            items = [
                QTableWidgetItem(t.get("id","")),
                QTableWidgetItem(t.get("beschreibung","")),
                QTableWidgetItem(t.get("projekt","")),
                QTableWidgetItem(t.get("status","")),
                QTableWidgetItem(str(t.get("dringlichkeit",""))),
                QTableWidgetItem(t.get("faellig_bis","")),
            ]
            for c, it in enumerate(items):
                # nicht editierbar
                it.setFlags(it.flags() & ~Qt.ItemIsEditable)
                table.setItem(r, c, it)

        table.setSortingEnabled(True)
        # Standard: nach ID aufsteigend (älteste zuerst)
        table.sortItems(0, Qt.AscendingOrder)


    def show_page(self, name: str):
        mapping = {
            "Home": self.pageHome,
            "Tasks": self.pageTasks,
            "Meetings": self.pageMeetings,
            "Questions": self.pageQuestions,
        }
        page = mapping.get(name)
        if not (self.stack and page):
            return
        self.stack.setCurrentWidget(page)
        if self.lblTitle:
            self.lblTitle.setText(name)
        # active-State togglen
        for btn_name, btn in {
            "Home": self.btnHome, "Tasks": self.btnTasks,
            "Meetings": self.btnMeetings, "Questions": self.btnQuestions,
        }.items():
            if btn:
                btn.setProperty("active", btn_name == name)
                btn.style().unpolish(btn); btn.style().polish(btn)
        
        
    # -------- Helper --------
    def setup_tables(self):
        """Einheitliches Verhalten der Tabellen (Stretch/Resize)."""

        def config_table(name: str, stretch_last=True) -> QTableWidget | None:
            t = self.root.findChild(QTableWidget, name)
            if not t:
                return None
            h: QHeaderView = t.horizontalHeader()
            h.setSectionResizeMode(QHeaderView.Interactive)  # manuell verschiebbar
            if stretch_last:
                h.setStretchLastSection(True)
            t.setWordWrap(False)
            return t

        # Home: "Heute fällig"
        config_table("tableDueToday", stretch_last=True)

        # Tasks: volle Liste
        # Tasks: volle Liste
        tt = config_table("tableAllTasks", stretch_last=False)   # <- NICHT die letzte Spalte stretchen
        if tt:
            h = tt.horizontalHeader()

            DESC_MIN = 320  # Mindestbreite für "Beschreibung"
            self._tasks_desc_min = DESC_MIN

            # Basis-Resizemodi: alles interaktiv …
            h.setSectionResizeMode(QHeaderView.Interactive)

            # … aber: "Beschreibung" soll strecken (nimmt den Restplatz)
            h.setSectionResizeMode(1, QHeaderView.Stretch)

            # "Prio" soll klein und fix sein
            h.setSectionResizeMode(4, QHeaderView.Fixed)
            tt.setColumnWidth(4, 56)

            # Initiale Breiten (werden als Start gesetzt)
            tt.setColumnWidth(0, 120)  # ID
            tt.setColumnWidth(2, 180)  # Projekt
            tt.setColumnWidth(3, 90)  # Status
            tt.setColumnWidth(4, 25)    # Prio
            tt.setColumnWidth(5, 100)  # Fällig

            # Anfangs-Mindestbreite für Beschreibung sicherstellen
            if tt.columnWidth(1) < DESC_MIN:
                h.resizeSection(1, DESC_MIN)

            # Event-Filter installieren, damit "Beschreibung" auch nach Resizes min. so groß bleibt
            if not hasattr(self, "_tasks_table"):
                self._tasks_table = tt
                tt.installEventFilter(self)


        # Meetings: Titel-Spalte breiter, letzte (Notizen) flexibel
        tm = config_table("tableMeetings", stretch_last=True)
        if tm:
            # Indexe: 0 Datum, 1 Zeit, 2 Titel, 3 Projekt, 4 Ort, 5 Aufgaben#, 6 Notizen
            tm.setColumnWidth(0, 90)
            tm.setColumnWidth(1, 80)
            tm.setColumnWidth(2, 260)  # Titel breiter
            tm.setColumnWidth(3, 120)
            tm.setColumnWidth(4, 100)
            tm.setColumnWidth(5, 90)
            # 6 (Notizen) streckt sich automatisch
            
    def on_task_new(self):
        from src.tasks.task_dialog import TaskDialog  # type: ignore
        from PySide6.QtWidgets import QMessageBox

        dlg = TaskDialog(self)
        dlg.show()  # nicht-modal öffnen

        def handle_saved():
            if dlg.created_id:
                QMessageBox.information(self, "Gespeichert", f"Neue Aufgabe erstellt: {dlg.created_id}")
                self.reload_tasks_views()  # <- Tabelle neu laden

        dlg.accepted.connect(handle_saved)

    def eventFilter(self, obj, event):
        # Mindestbreite der "Beschreibung"-Spalte in tableAllTasks durchsetzen
        try:
            from PySide6.QtCore import QEvent
            if obj is getattr(self, "_tasks_table", None) and event.type() == QEvent.Resize:
                tt = self._tasks_table
                h = tt.horizontalHeader()
                desc_idx = 1
                min_w = getattr(self, "_tasks_desc_min", 320)
                if tt.columnWidth(desc_idx) < min_w:
                    h.resizeSection(desc_idx, min_w)
        except Exception:
            pass
        return super().eventFilter(obj, event)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.setWindowTitle("Heartli OfficeTool")
    w.resize(1200, 800)
    w.show()
    sys.exit(app.exec())
