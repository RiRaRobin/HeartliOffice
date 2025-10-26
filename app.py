from __future__ import annotations
import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QPushButton, QSplitter,
    QHeaderView, QWidget, QLabel
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt
from PySide6.QtWidgets import QHeaderView, QTableWidget, QMessageBox, QTableWidgetItem, QAbstractItemView, QCheckBox, QHBoxLayout, QVBoxLayout, QScrollArea, QLineEdit
from PySide6.QtGui import QColor, QBrush, QShortcut, QKeySequence
from datetime import date, datetime
from src.tasks.task_dialog import TaskDialog # type: ignore
from src.tasks.tasks_service import load_tasks_active, load_task, archive_task # type: ignore

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
        
        self.leTaskSearch = self.root.findChild(QLineEdit, "leTaskSearch")
        self.btnTaskApply = self.root.findChild(QPushButton, "btnTaskApply")

        self._search_text = ""

        if self.btnTaskApply:
            self.btnTaskApply.clicked.connect(self.on_task_apply_search)
        if self.leTaskSearch:
            self.leTaskSearch.returnPressed.connect(self.on_task_apply_search)

        # Clicks verdrahten
        if self.btnHome:      self.btnHome.clicked.connect(lambda: self.show_page("Home"))
        if self.btnTasks:     self.btnTasks.clicked.connect(lambda: self.show_page("Tasks"))
        if self.btnMeetings:  self.btnMeetings.clicked.connect(lambda: self.show_page("Meetings"))
        if self.btnQuestions: self.btnQuestions.clicked.connect(lambda: self.show_page("Questions"))
        
        self.btnTaskEdit = self.root.findChild(QPushButton, "btnTaskEdit")
        if self.btnTaskEdit:
            self.btnTaskEdit.clicked.connect(self.on_task_edit)

        # Doppelklick auf Zeile öffnet Bearbeiten
        table = self.root.findChild(QTableWidget, "tableAllTasks")
        if table:
            table.itemDoubleClicked.connect(lambda _item: self.on_task_edit())

        # Button Archive
        self.btnTaskArchive = self.root.findChild(QPushButton, "btnTaskArchive")
        if self.btnTaskArchive:
            self.btnTaskArchive.clicked.connect(self.on_task_archive)
        
        # Tabellen-Setup optional
        self.setup_tables()
        
        # --- Suchfeld & Filter initialisieren ---
        self.leTaskSearch = self.root.findChild(QLineEdit, "leTaskSearch")
        self.btnTaskApply = self.root.findChild(QPushButton, "btnTaskApply")
        self._search_text = ""

        if self.btnTaskApply:
            # Klick auf "Anwenden" löst Suche aus
            self.btnTaskApply.clicked.connect(self.on_task_apply_search)

        if self.leTaskSearch:
            # Enter im Feld startet Suche
            self.leTaskSearch.returnPressed.connect(self.on_task_apply_search)

            # 🟢 Live-Search: Filtert während der Eingabe
            self.leTaskSearch.textChanged.connect(lambda _:
                setattr(self, "_search_text", self.leTaskSearch.text().strip()) or self.reload_tasks_views()
            )
        
        # --- Projekt-Filter State
        self._project_checks: dict[str, QCheckBox] = {}
        self._cbAll: QCheckBox | None = None
        self._project_filter_active: set[str] | None = None  # None = kein Filter (alles zeigen)
        
        self._search_text: str = ""

        # Filter-UI bauen (aus den vorhandenen YAMLs)
        self.build_project_filters()

        # Aktiven Button optisch markieren (optional)
        self.setStyleSheet("""
            QPushButton[active="true"] { background: #1f2937; color: #e5e7eb; border-radius: 8px; }
            QPushButton:hover { background: #111827; }
        """)
        
        self.show_page("Home")
        self.reload_tasks_views()
        
        # --- Tastatur-Shortcuts ---
        self.tableAll = self.root.findChild(QTableWidget, "tableAllTasks")

        self._shortcuts = [
            QShortcut(QKeySequence("Ctrl+N"), self, activated=self.on_task_new),
            QShortcut(QKeySequence("Delete"), self, activated=self.on_task_archive),
            QShortcut(QKeySequence("Ctrl+R"), self, activated=self.reset_task_filters),
            QShortcut(QKeySequence("Ctrl+F"), self,
                    activated=lambda: (self.leTaskSearch.setFocus() if self.leTaskSearch else None)),
        ]
        # Enter nur auf der Tabelle aktivieren
        if self.tableAll:
            self._sc_enter = QShortcut(QKeySequence("Return"), self.tableAll, activated=self.on_task_edit)


    # ----------------------------------------------------------
    #   Alle Tasks in Tabelle anzeigen
    # ----------------------------------------------------------
    def _current_rows(self) -> list[dict]:
        """Lädt aktive Tasks und wendet Projekt- und Textfilter an."""
        rows = load_tasks_active()

        # Projektfilter
        if getattr(self, "_project_filter_active", None) is not None:
            rows = [r for r in rows if (r.get("projekt") or "") in self._project_filter_active]

        # Textsuche (case-insensitive)
        q = (getattr(self, "_search_text", "") or "").strip().lower()
        if q:
            def norm(x): return (str(x) if x is not None else "").lower()
            KEYS = ("id", "beschreibung", "projekt", "status", "notizen", "follow_up")
            rows = [t for t in rows if any(q in norm(t.get(k, "")) for k in KEYS)]

        return rows
    
    def reload_tasks_views(self):
        """Füllt die Tasks-Tabelle neu (Alle Tasks)."""
        table = self.root.findChild(QTableWidget, "tableAllTasks")
        if not table:
            return

        rows = self._current_rows()
        
        # --- Projekt-Filter anwenden ---
        if self._project_filter_active is not None:
            rows = [
                r for r in rows
                if (r.get("projekt") or "") in self._project_filter_active
            ]

        # --- Textsuche anwenden ---
        q = (self._search_text or "").lower()
        if q:
            def match(t: dict) -> bool:
                return any(
                    q in (str(t.get(k, "")) or "").lower()
                    for k in ("beschreibung", "projekt", "status", "notizen", "follow_up", "id")
                )
            rows = [t for t in rows if match(t)]
        
        # ---------- "Heute fällig" unten füllen ----------
        table_today = self.root.findChild(QTableWidget, "tableDueToday")
        if table_today:
            # Filtere die gleichen rows auf Fälligkeit == heute
            today = date.today()
            def parse_date(s: str):
                try:
                    return datetime.strptime(s, "%Y-%m-%d").date()
                except Exception:
                    return None
            today = date.today()
            due_today = [t for t in rows if parse_date(str(t.get("faellig_bis","")).strip()) == today]

            due_today = []
            today = date.today()
            for t in rows:  # ← gefilterte rows
                fb = str(t.get("faellig_bis", "")).strip()
                try:
                    d = datetime.strptime(fb, "%Y-%m-%d").date()
                except Exception:
                    d = None
                if d == today:
                    due_today.append(t)

            table_today.setSortingEnabled(False)
            table_today.clearContents()
            table_today.setRowCount(len(due_today))

            for r, t in enumerate(due_today):
                items = [
                    QTableWidgetItem(t.get("id","")),
                    QTableWidgetItem(t.get("beschreibung","")),
                    QTableWidgetItem(t.get("projekt","")),
                    QTableWidgetItem(t.get("status","")),
                    QTableWidgetItem(str(t.get("dringlichkeit",""))),
                    QTableWidgetItem(t.get("faellig_bis","")),
                ]
                # heute = rot
                color = QColor("#ef4444")
                for it in items:
                    it.setFlags(it.flags() & ~Qt.ItemIsEditable)
                    it.setForeground(QBrush(color))
                for c, it in enumerate(items):
                    table_today.setItem(r, c, it)

            table_today.setSortingEnabled(True)
            table_today.sortItems(0, Qt.AscendingOrder)
        
        # ▼▼ Projektsicht filtern, wenn aktiv ▼▼
        if self._project_filter_active is not None:
            rows = [
                r for r in rows
                if (r.get("projekt") or "") in self._project_filter_active
            ]

        # Spalten: 0 ID | 1 Beschreibung | 2 Projekt | 3 Status | 4 Prio | 5 Fällig
        table.setSortingEnabled(False)
        table.clearContents()
        table.setRowCount(len(rows))

        for r, t in enumerate(rows):
            faellig_raw = str(t.get("faellig_bis", "")).strip()
            color = None

            # Fälligkeit prüfen
            if faellig_raw:
                try:
                    faellig = datetime.strptime(faellig_raw, "%Y-%m-%d").date()
                    today = date.today()
                    if faellig < today:
                        color = QColor("#b91c1c")   # dunkelrot: überfällig
                    elif faellig == today:
                        color = QColor("#ef4444")   # rot: heute fällig
                except Exception:
                    pass

            items = [
                QTableWidgetItem(t.get("id","")),
                QTableWidgetItem(t.get("beschreibung","")),
                QTableWidgetItem(t.get("projekt","")),
                QTableWidgetItem(t.get("status","")),
                QTableWidgetItem(str(t.get("dringlichkeit",""))),
                QTableWidgetItem(faellig_raw),
            ]

            for c, it in enumerate(items):
                it.setFlags(it.flags() & ~Qt.ItemIsEditable)
                # Farbe anwenden (alle Spalten einfärben)
                if color:
                    it.setForeground(QBrush(color))
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
            h.setSectionResizeMode(QHeaderView.Interactive)
            if stretch_last:
                h.setStretchLastSection(True)
            t.setWordWrap(False)
            return t

        # Home
        config_table("tableDueToday", stretch_last=True)

        # Tasks – volle Liste
        tt = config_table("tableAllTasks", stretch_last=False)   # nicht die letzte Spalte stretchen
        if tt:
            # Auswahl: ganze Zeile, Single
            tt.setSelectionBehavior(QAbstractItemView.SelectRows)
            tt.setSelectionMode(QAbstractItemView.SingleSelection)

            h = tt.horizontalHeader()

            DESC_MIN = 320  # Mindestbreite für "Beschreibung"
            self._tasks_desc_min = DESC_MIN

            # Basis: interaktiv …
            h.setSectionResizeMode(QHeaderView.Interactive)

            # … aber "Beschreibung" (Spalte 1) streckt den Restplatz
            h.setSectionResizeMode(1, QHeaderView.Stretch)

            # "Prio" (Spalte 4) klein & fix
            h.setSectionResizeMode(4, QHeaderView.Fixed)
            tt.setColumnWidth(4, 56)   # ← wähle EINEN Wert; 25 war zu klein

            # Initiale Breiten
            tt.setColumnWidth(0, 120)  # ID
            tt.setColumnWidth(2, 180)  # Projekt
            tt.setColumnWidth(3, 90)   # Status
            tt.setColumnWidth(5, 100)  # Fällig

            # Mindestbreite Beschreibung sicherstellen
            if tt.columnWidth(1) < DESC_MIN:
                h.resizeSection(1, DESC_MIN)

            # Event-Filter für Mindestbreite
            if not hasattr(self, "_tasks_table"):
                self._tasks_table = tt
                tt.installEventFilter(self)

        # Meetings
        tm = config_table("tableMeetings", stretch_last=True)
        if tm:
            tm.setColumnWidth(0, 90)
            tm.setColumnWidth(1, 80)
            tm.setColumnWidth(2, 260)
            tm.setColumnWidth(3, 120)
            tm.setColumnWidth(4, 100)
            tm.setColumnWidth(5, 90)
        
        # Questions: Tabelle konfigurieren
        tq = self.root.findChild(QTableWidget, "tableQuestions")
        if tq:
            h: QHeaderView = tq.horizontalHeader()

            # 1) GANZ WICHTIG: Last-Section-Stretch ausschalten (überschreibt UI-Attribut)
            h.setStretchLastSection(False)

            tq.setWordWrap(False)
            tq.setSelectionBehavior(QTableWidget.SelectRows)
            tq.setSelectionMode(QTableWidget.SingleSelection)

            # 2) Resize-Modi pro Spalte setzen
            h.setSectionResizeMode(0, QHeaderView.Fixed)     # Person = fix
            h.setSectionResizeMode(1, QHeaderView.Stretch)   # Frage = dynamisch (füllt Rest)
            h.setSectionResizeMode(2, QHeaderView.Fixed)     # Status = fix
            h.setSectionResizeMode(3, QHeaderView.Fixed)     # Typ = fix

            # 3) Fixbreiten setzen (min. Breite beachten)
            # h.setMinimumSectionSize(20)  # optional, falls 10px gewünscht
            tq.setColumnWidth(0, 120)    # Person
            tq.setColumnWidth(2, 90)     # Status
            tq.setColumnWidth(3, 100)     # Typ (jetzt bleibt klein)
            
    def on_task_new(self):
        from PySide6.QtWidgets import QMessageBox
        try:
            from src.tasks.task_dialog import TaskDialog  # type: ignore
            dlg = TaskDialog(self)        # create mode
            dlg.show()                    # nicht-modal
            def handle_saved():
                if dlg.created_id:
                    QMessageBox.information(self, "Gespeichert", f"Neue Aufgabe erstellt: {dlg.created_id}")
                    # 🔧 Projektfilter aktualisieren, bevor Tabelle neu geladen wird
                    self.build_project_filters()
                    self.reload_tasks_views()
            dlg.accepted.connect(handle_saved)
        except Exception as e:
            QMessageBox.critical(self, "Fehler beim Öffnen", str(e))

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

    def _selected_task_id(self) -> str | None:
        table = self.root.findChild(QTableWidget, "tableAllTasks")
        if not table:
            return None
        sel = table.selectedItems()
        if not sel:
            return None
        row = sel[0].row()
        item = table.item(row, 0)  # Spalte 0 = ID
        return item.text() if item else None

    def on_task_edit(self):
        tid = self._selected_task_id()
        if not tid:
            QMessageBox.warning(self, "Hinweis", "Bitte zuerst eine Aufgabe auswählen.")
            return
        try:
            t = load_task(tid)
        except FileNotFoundError:
            QMessageBox.warning(self, "Fehler", f"Task-Datei zu {tid} nicht gefunden.")
            return

        dlg = TaskDialog(self, mode="edit", task=t)
        dlg.show()  # nicht-modal
        def after_edit():
            self.reload_tasks_views()
        dlg.accepted.connect(after_edit)
    
    def _selected_task_id(self) -> str | None:
        table = self.root.findChild(QTableWidget, "tableAllTasks")
        if not table:
            return None
        sel = table.selectedItems()
        if not sel:
            return None
        row = sel[0].row()
        item = table.item(row, 0)  # Spalte 0 = ID
        return item.text() if item else None
    
    def on_task_archive(self):
        tid = self._selected_task_id()
        if not tid:
            QMessageBox.information(self, "Hinweis", "Bitte zuerst eine Aufgabe in der Liste auswählen.")
            return

        resp = QMessageBox.question(
            self, "Archivieren",
            f"Soll die Aufgabe {tid} ins Archiv verschoben werden?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if resp != QMessageBox.Yes:
            return

        try:
            archive_task(tid)
        except FileNotFoundError:
            QMessageBox.warning(self, "Fehler", f"Task-Datei zu {tid} wurde nicht gefunden.")
            return
        except Exception as e:
            QMessageBox.critical(self, "Fehler beim Archivieren", str(e))
            return

        QMessageBox.information(self, "Archiviert", f"{tid} wurde ins Archiv verschoben.")
        self.build_project_filters()
        self.reload_tasks_views()
        
    def build_project_filters(self):
        """Erzeugt/aktualisiert die Projekt-Checkboxen oberhalb der Task-Tabelle."""
        # Projekte aus YAMLs sammeln
        projects = sorted({(t.get("projekt") or "") for t in load_tasks_active()})

        # Platzhalter-Container im UI suchen; wenn nicht vorhanden, oben in pageTasks anlegen
        container = self.root.findChild(QWidget, "panelTaskFilters")
        if container is None:
            container = QWidget(self.pageTasks)
            container.setObjectName("panelTaskFilters")
            # sicherstellen, dass pageTasks ein Layout hat
            lay = self.pageTasks.layout()
            if lay is None:
                lay = QVBoxLayout(self.pageTasks)
            # Container ganz oben einsetzen (über der Tabelle)
            lay.insertWidget(0, container)

        # Layout im Container vorbereiten/aufräumen
        layout = container.layout()
        if layout is None:
            layout = QHBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(8)
        else:
            # alte Widgets entfernen
            while layout.count():
                item = layout.takeAt(0)
                w = item.widget()
                if w:
                    w.setParent(None)

        # "Alle" Checkbox
        self._project_checks.clear()
        self._cbAll = QCheckBox("Alle", container)
        self._cbAll.setChecked(True)

        def on_toggle_all_clicked():
            # wenn NICHT alle an sind -> alle AN, sonst alle AUS
            all_on = all(cb.isChecked() for cb in self._project_checks.values())
            target = not all_on
            for cb in self._project_checks.values():
                cb.blockSignals(True)
                cb.setChecked(target)
                cb.blockSignals(False)
            self.on_filter_changed()

        self._cbAll.clicked.connect(on_toggle_all_clicked)
        layout.addWidget(self._cbAll)

        # Einzel-Projekt-Checkboxen
        for p in projects:
            label = p if p else "(ohne Projekt)"
            cb = QCheckBox(label, container)
            cb.setChecked(True)
            # wichtig: Wert binden!
            cb.stateChanged.connect(lambda _s, value=p: self.on_single_project_changed(value))
            layout.addWidget(cb)
            self._project_checks[p] = cb

        layout.addStretch()

        # initial: alle aktiv
        self._project_filter_active = set(projects)

    def on_single_project_changed(self, project_value: str):
        # Status der „Alle“-Checkbox synchronisieren und neu laden
        self.on_filter_changed()

    def on_filter_changed(self):
        # aktive Menge auslesen
        active: set[str] = set()
        for value, cb in self._project_checks.items():
            if cb.isChecked():
                active.add(value)
        self._project_filter_active = active

        # „Alle“-Checkbox setzen, ohne Re-Signal
        if self._cbAll:
            all_on = len(active) == len(self._project_checks)
            self._cbAll.blockSignals(True)
            self._cbAll.setChecked(all_on)
            self._cbAll.blockSignals(False)

        # Tabelle neu füllen
        self.reload_tasks_views()
        
    def on_task_apply_search(self):
        self._search_text = (self.leTaskSearch.text().strip() if self.leTaskSearch else "")
        # optional: beim Suchen direkt auf Tasks-Ansicht springen
        self.show_page("Tasks")
        self.reload_tasks_views()
        
    def reset_task_filters(self):
        """Setzt Suche + Projektfilter zurück und lädt Tabelle neu."""
        # Suche leeren
        self._search_text = ""
        if self.leTaskSearch:
            self.leTaskSearch.clear()

        # Alle Projekte aktivieren
        if hasattr(self, "_project_checks"):
            for cb in self._project_checks.values():
                cb.blockSignals(True)
                cb.setChecked(True)
                cb.blockSignals(False)
            self._project_filter_active = set(self._project_checks.keys())

        if hasattr(self, "_cbAll") and self._cbAll:
            self._cbAll.blockSignals(True)
            self._cbAll.setChecked(True)
            self._cbAll.blockSignals(False)

        self.reload_tasks_views()
        
    def _current_rows(self) -> list[dict]:
        rows = load_tasks_active()

        # Projekt-Filter
        if self._project_filter_active is not None:
            rows = [r for r in rows if (r.get("projekt") or "") in self._project_filter_active]

        # Textsuche
        q = (self._search_text or "").strip().lower()
        if q:
            def norm(x): return (str(x) if x is not None else "").lower()
            KEYS = ("id", "beschreibung", "projekt", "status", "notizen", "follow_up")
            rows = [t for t in rows if any(q in norm(t.get(k, "")) for k in KEYS)]

        return rows


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.setWindowTitle("Heartli OfficeTool")
    w.resize(1200, 800)
    w.show()
    sys.exit(app.exec())
