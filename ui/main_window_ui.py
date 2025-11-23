# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QMenuBar, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QSplitter,
    QStackedWidget, QStatusBar, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1301, 791)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.main_vbox = QVBoxLayout(self.centralwidget)
        self.main_vbox.setSpacing(8)
        self.main_vbox.setObjectName(u"main_vbox")
        self.header_hbox = QHBoxLayout()
        self.header_hbox.setObjectName(u"header_hbox")
        self.lblTitle = QLabel(self.centralwidget)
        self.lblTitle.setObjectName(u"lblTitle")

        self.header_hbox.addWidget(self.lblTitle)

        self.sp_header = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.header_hbox.addItem(self.sp_header)

        self.leSearch = QLineEdit(self.centralwidget)
        self.leSearch.setObjectName(u"leSearch")

        self.header_hbox.addWidget(self.leSearch)


        self.main_vbox.addLayout(self.header_hbox)

        self.body_splitter = QSplitter(self.centralwidget)
        self.body_splitter.setObjectName(u"body_splitter")
        self.body_splitter.setOrientation(Qt.Orientation.Horizontal)
        self.body_splitter.setHandleWidth(6)
        self.body_splitter.setChildrenCollapsible(False)
        self.sidePanel = QWidget(self.body_splitter)
        self.sidePanel.setObjectName(u"sidePanel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sidePanel.sizePolicy().hasHeightForWidth())
        self.sidePanel.setSizePolicy(sizePolicy)
        self.sidePanel.setMinimumSize(QSize(220, 0))
        self.sidePanel.setMaximumSize(QSize(220, 16777215))
        self.side_vbox = QVBoxLayout(self.sidePanel)
        self.side_vbox.setSpacing(6)
        self.side_vbox.setObjectName(u"side_vbox")
        self.side_vbox.setContentsMargins(0, 0, 0, 0)
        self.btnNavHome = QPushButton(self.sidePanel)
        self.btnNavHome.setObjectName(u"btnNavHome")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btnNavHome.sizePolicy().hasHeightForWidth())
        self.btnNavHome.setSizePolicy(sizePolicy1)
        self.btnNavHome.setMinimumSize(QSize(0, 24))

        self.side_vbox.addWidget(self.btnNavHome)

        self.btnNavTasks = QPushButton(self.sidePanel)
        self.btnNavTasks.setObjectName(u"btnNavTasks")
        sizePolicy1.setHeightForWidth(self.btnNavTasks.sizePolicy().hasHeightForWidth())
        self.btnNavTasks.setSizePolicy(sizePolicy1)
        self.btnNavTasks.setMinimumSize(QSize(0, 24))

        self.side_vbox.addWidget(self.btnNavTasks)

        self.btnNavMeetings = QPushButton(self.sidePanel)
        self.btnNavMeetings.setObjectName(u"btnNavMeetings")
        sizePolicy1.setHeightForWidth(self.btnNavMeetings.sizePolicy().hasHeightForWidth())
        self.btnNavMeetings.setSizePolicy(sizePolicy1)
        self.btnNavMeetings.setMinimumSize(QSize(0, 24))

        self.side_vbox.addWidget(self.btnNavMeetings)

        self.btnNavQuestions = QPushButton(self.sidePanel)
        self.btnNavQuestions.setObjectName(u"btnNavQuestions")
        sizePolicy1.setHeightForWidth(self.btnNavQuestions.sizePolicy().hasHeightForWidth())
        self.btnNavQuestions.setSizePolicy(sizePolicy1)
        self.btnNavQuestions.setMinimumSize(QSize(0, 24))

        self.side_vbox.addWidget(self.btnNavQuestions)

        self.btnNavFiles = QPushButton(self.sidePanel)
        self.btnNavFiles.setObjectName(u"btnNavFiles")

        self.side_vbox.addWidget(self.btnNavFiles)

        self.sp_side_bottom = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.side_vbox.addItem(self.sp_side_bottom)

        self.body_splitter.addWidget(self.sidePanel)
        self.content = QWidget(self.body_splitter)
        self.content.setObjectName(u"content")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.content.sizePolicy().hasHeightForWidth())
        self.content.setSizePolicy(sizePolicy2)
        self.content_vbox = QVBoxLayout(self.content)
        self.content_vbox.setSpacing(8)
        self.content_vbox.setObjectName(u"content_vbox")
        self.content_vbox.setContentsMargins(0, 0, 0, 0)
        self.mainStack = QStackedWidget(self.content)
        self.mainStack.setObjectName(u"mainStack")
        self.pageHome = QWidget()
        self.pageHome.setObjectName(u"pageHome")
        self.pageHome_vbox = QVBoxLayout(self.pageHome)
        self.pageHome_vbox.setSpacing(8)
        self.pageHome_vbox.setObjectName(u"pageHome_vbox")
        self.home_grid = QGridLayout()
        self.home_grid.setSpacing(8)
        self.home_grid.setObjectName(u"home_grid")
        self.boxStats = QGroupBox(self.pageHome)
        self.boxStats.setObjectName(u"boxStats")
        self.boxStats_vbox = QVBoxLayout(self.boxStats)
        self.boxStats_vbox.setObjectName(u"boxStats_vbox")
        self.lblOpenCount = QLabel(self.boxStats)
        self.lblOpenCount.setObjectName(u"lblOpenCount")

        self.boxStats_vbox.addWidget(self.lblOpenCount)

        self.lblArchivedWeek = QLabel(self.boxStats)
        self.lblArchivedWeek.setObjectName(u"lblArchivedWeek")

        self.boxStats_vbox.addWidget(self.lblArchivedWeek)


        self.home_grid.addWidget(self.boxStats, 0, 0, 1, 1)

        self.boxUrgency = QGroupBox(self.pageHome)
        self.boxUrgency.setObjectName(u"boxUrgency")
        self.boxUrgency_vbox = QVBoxLayout(self.boxUrgency)
        self.boxUrgency_vbox.setObjectName(u"boxUrgency_vbox")
        self.chartUrgencyHolder = QWidget(self.boxUrgency)
        self.chartUrgencyHolder.setObjectName(u"chartUrgencyHolder")
        sizePolicy2.setHeightForWidth(self.chartUrgencyHolder.sizePolicy().hasHeightForWidth())
        self.chartUrgencyHolder.setSizePolicy(sizePolicy2)

        self.boxUrgency_vbox.addWidget(self.chartUrgencyHolder)


        self.home_grid.addWidget(self.boxUrgency, 0, 1, 1, 1)


        self.pageHome_vbox.addLayout(self.home_grid)

        self.boxDueToday = QGroupBox(self.pageHome)
        self.boxDueToday.setObjectName(u"boxDueToday")
        self.boxDueToday_vbox = QVBoxLayout(self.boxDueToday)
        self.boxDueToday_vbox.setObjectName(u"boxDueToday_vbox")
        self.tableDueToday = QTableWidget(self.boxDueToday)
        if (self.tableDueToday.columnCount() < 6):
            self.tableDueToday.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableDueToday.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableDueToday.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableDueToday.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableDueToday.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableDueToday.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableDueToday.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        self.tableDueToday.setObjectName(u"tableDueToday")
        self.tableDueToday.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableDueToday.setAlternatingRowColors(True)
        self.tableDueToday.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tableDueToday.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableDueToday.setSortingEnabled(True)

        self.boxDueToday_vbox.addWidget(self.tableDueToday)


        self.pageHome_vbox.addWidget(self.boxDueToday)

        self.pageHome_vbox.setStretch(1, 1)
        self.mainStack.addWidget(self.pageHome)
        self.pageFiles = QWidget()
        self.pageFiles.setObjectName(u"pageFiles")
        self.verticalLayout = QVBoxLayout(self.pageFiles)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.boxFilesFilters = QGroupBox(self.pageFiles)
        self.boxFilesFilters.setObjectName(u"boxFilesFilters")
        self.horizontalLayout = QHBoxLayout(self.boxFilesFilters)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelProject = QLabel(self.boxFilesFilters)
        self.labelProject.setObjectName(u"labelProject")

        self.horizontalLayout.addWidget(self.labelProject)

        self.cbFilesProject = QComboBox(self.boxFilesFilters)
        self.cbFilesProject.setObjectName(u"cbFilesProject")

        self.horizontalLayout.addWidget(self.cbFilesProject)

        self.labelSuche = QLabel(self.boxFilesFilters)
        self.labelSuche.setObjectName(u"labelSuche")

        self.horizontalLayout.addWidget(self.labelSuche)

        self.leFilesSearch = QLineEdit(self.boxFilesFilters)
        self.leFilesSearch.setObjectName(u"leFilesSearch")

        self.horizontalLayout.addWidget(self.leFilesSearch)

        self.btnFilesApply = QPushButton(self.boxFilesFilters)
        self.btnFilesApply.setObjectName(u"btnFilesApply")

        self.horizontalLayout.addWidget(self.btnFilesApply)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btnFileNew = QPushButton(self.boxFilesFilters)
        self.btnFileNew.setObjectName(u"btnFileNew")

        self.horizontalLayout.addWidget(self.btnFileNew)

        self.btnFileEdit = QPushButton(self.boxFilesFilters)
        self.btnFileEdit.setObjectName(u"btnFileEdit")

        self.horizontalLayout.addWidget(self.btnFileEdit)


        self.verticalLayout.addWidget(self.boxFilesFilters)

        self.tableFiles = QTableWidget(self.pageFiles)
        if (self.tableFiles.columnCount() < 8):
            self.tableFiles.setColumnCount(8)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableFiles.setHorizontalHeaderItem(0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableFiles.setHorizontalHeaderItem(1, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableFiles.setHorizontalHeaderItem(2, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableFiles.setHorizontalHeaderItem(3, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableFiles.setHorizontalHeaderItem(4, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableFiles.setHorizontalHeaderItem(5, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableFiles.setHorizontalHeaderItem(6, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableFiles.setHorizontalHeaderItem(7, __qtablewidgetitem13)
        self.tableFiles.setObjectName(u"tableFiles")
        self.tableFiles.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableFiles.setAlternatingRowColors(True)
        self.tableFiles.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tableFiles.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableFiles.setSortingEnabled(True)
        self.tableFiles.setColumnCount(8)

        self.verticalLayout.addWidget(self.tableFiles)

        self.mainStack.addWidget(self.pageFiles)
        self.pageTasks = QWidget()
        self.pageTasks.setObjectName(u"pageTasks")
        self.pageTasks_vbox = QVBoxLayout(self.pageTasks)
        self.pageTasks_vbox.setSpacing(8)
        self.pageTasks_vbox.setObjectName(u"pageTasks_vbox")
        self.tasks_top_grid = QGridLayout()
        self.tasks_top_grid.setSpacing(8)
        self.tasks_top_grid.setObjectName(u"tasks_top_grid")
        self.boxTasksStats = QGroupBox(self.pageTasks)
        self.boxTasksStats.setObjectName(u"boxTasksStats")
        self.boxTasksStats_vbox = QVBoxLayout(self.boxTasksStats)
        self.boxTasksStats_vbox.setObjectName(u"boxTasksStats_vbox")
        self.lblOpenCountTasks = QLabel(self.boxTasksStats)
        self.lblOpenCountTasks.setObjectName(u"lblOpenCountTasks")

        self.boxTasksStats_vbox.addWidget(self.lblOpenCountTasks)

        self.lblArchivedWeekTasks = QLabel(self.boxTasksStats)
        self.lblArchivedWeekTasks.setObjectName(u"lblArchivedWeekTasks")

        self.boxTasksStats_vbox.addWidget(self.lblArchivedWeekTasks)


        self.tasks_top_grid.addWidget(self.boxTasksStats, 0, 0, 1, 1)

        self.boxUrgencyTasks = QGroupBox(self.pageTasks)
        self.boxUrgencyTasks.setObjectName(u"boxUrgencyTasks")
        self.boxUrgencyTasks_vbox = QVBoxLayout(self.boxUrgencyTasks)
        self.boxUrgencyTasks_vbox.setObjectName(u"boxUrgencyTasks_vbox")
        self.chartUrgencyTasksHolder = QWidget(self.boxUrgencyTasks)
        self.chartUrgencyTasksHolder.setObjectName(u"chartUrgencyTasksHolder")
        sizePolicy2.setHeightForWidth(self.chartUrgencyTasksHolder.sizePolicy().hasHeightForWidth())
        self.chartUrgencyTasksHolder.setSizePolicy(sizePolicy2)

        self.boxUrgencyTasks_vbox.addWidget(self.chartUrgencyTasksHolder)


        self.tasks_top_grid.addWidget(self.boxUrgencyTasks, 0, 1, 1, 1)


        self.pageTasks_vbox.addLayout(self.tasks_top_grid)

        self.boxTasksFilters = QGroupBox(self.pageTasks)
        self.boxTasksFilters.setObjectName(u"boxTasksFilters")
        self.boxTasksFilters_hbox = QHBoxLayout(self.boxTasksFilters)
        self.boxTasksFilters_hbox.setObjectName(u"boxTasksFilters_hbox")
        self.scrollProjects = QScrollArea(self.boxTasksFilters)
        self.scrollProjects.setObjectName(u"scrollProjects")
        self.scrollProjects.setWidgetResizable(True)
        self.scrollProjectsContents = QWidget()
        self.scrollProjectsContents.setObjectName(u"scrollProjectsContents")
        self.scrollProjectsContents.setGeometry(QRect(0, 0, 181, 40))
        self.projectsChecks_vbox = QVBoxLayout(self.scrollProjectsContents)
        self.projectsChecks_vbox.setObjectName(u"projectsChecks_vbox")
        self.lblProjectsHint = QLabel(self.scrollProjectsContents)
        self.lblProjectsHint.setObjectName(u"lblProjectsHint")

        self.projectsChecks_vbox.addWidget(self.lblProjectsHint)

        self.sp_proj = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.projectsChecks_vbox.addItem(self.sp_proj)

        self.scrollProjects.setWidget(self.scrollProjectsContents)

        self.boxTasksFilters_hbox.addWidget(self.scrollProjects)

        self.sp_mid = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.boxTasksFilters_hbox.addItem(self.sp_mid)

        self.tasks_actions_hbox = QHBoxLayout()
        self.tasks_actions_hbox.setObjectName(u"tasks_actions_hbox")
        self.leTaskSearch = QLineEdit(self.boxTasksFilters)
        self.leTaskSearch.setObjectName(u"leTaskSearch")

        self.tasks_actions_hbox.addWidget(self.leTaskSearch)

        self.btnTasksApply = QPushButton(self.boxTasksFilters)
        self.btnTasksApply.setObjectName(u"btnTasksApply")

        self.tasks_actions_hbox.addWidget(self.btnTasksApply)

        self.sp_act = QSpacerItem(16, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.tasks_actions_hbox.addItem(self.sp_act)

        self.btnTaskNew = QPushButton(self.boxTasksFilters)
        self.btnTaskNew.setObjectName(u"btnTaskNew")

        self.tasks_actions_hbox.addWidget(self.btnTaskNew)

        self.btnTaskEdit = QPushButton(self.boxTasksFilters)
        self.btnTaskEdit.setObjectName(u"btnTaskEdit")

        self.tasks_actions_hbox.addWidget(self.btnTaskEdit)

        self.btnTaskArchive = QPushButton(self.boxTasksFilters)
        self.btnTaskArchive.setObjectName(u"btnTaskArchive")

        self.tasks_actions_hbox.addWidget(self.btnTaskArchive)


        self.boxTasksFilters_hbox.addLayout(self.tasks_actions_hbox)


        self.pageTasks_vbox.addWidget(self.boxTasksFilters)

        self.boxAllTasks = QGroupBox(self.pageTasks)
        self.boxAllTasks.setObjectName(u"boxAllTasks")
        self.boxAllTasks_vbox = QVBoxLayout(self.boxAllTasks)
        self.boxAllTasks_vbox.setObjectName(u"boxAllTasks_vbox")
        self.tableAllTasks = QTableWidget(self.boxAllTasks)
        if (self.tableAllTasks.columnCount() < 6):
            self.tableAllTasks.setColumnCount(6)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tableAllTasks.setHorizontalHeaderItem(0, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tableAllTasks.setHorizontalHeaderItem(1, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.tableAllTasks.setHorizontalHeaderItem(2, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.tableAllTasks.setHorizontalHeaderItem(3, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.tableAllTasks.setHorizontalHeaderItem(4, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.tableAllTasks.setHorizontalHeaderItem(5, __qtablewidgetitem19)
        self.tableAllTasks.setObjectName(u"tableAllTasks")
        self.tableAllTasks.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableAllTasks.setAlternatingRowColors(True)
        self.tableAllTasks.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tableAllTasks.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableAllTasks.setSortingEnabled(True)

        self.boxAllTasks_vbox.addWidget(self.tableAllTasks)


        self.pageTasks_vbox.addWidget(self.boxAllTasks)

        self.pageTasks_vbox.setStretch(2, 1)
        self.mainStack.addWidget(self.pageTasks)
        self.pageMeetings = QWidget()
        self.pageMeetings.setObjectName(u"pageMeetings")
        self.pageMeetings_vbox = QVBoxLayout(self.pageMeetings)
        self.pageMeetings_vbox.setSpacing(8)
        self.pageMeetings_vbox.setObjectName(u"pageMeetings_vbox")
        self.boxMeetingsFilters = QGroupBox(self.pageMeetings)
        self.boxMeetingsFilters.setObjectName(u"boxMeetingsFilters")
        self.boxMeetingsFilters_hbox = QHBoxLayout(self.boxMeetingsFilters)
        self.boxMeetingsFilters_hbox.setObjectName(u"boxMeetingsFilters_hbox")
        self.scrollProjectsMeetings = QScrollArea(self.boxMeetingsFilters)
        self.scrollProjectsMeetings.setObjectName(u"scrollProjectsMeetings")
        self.scrollProjectsMeetings.setWidgetResizable(True)
        self.scrollProjectsMeetingsContents = QWidget()
        self.scrollProjectsMeetingsContents.setObjectName(u"scrollProjectsMeetingsContents")
        self.scrollProjectsMeetingsContents.setGeometry(QRect(0, 0, 181, 40))
        self.projectsMeetingsChecks_vbox = QVBoxLayout(self.scrollProjectsMeetingsContents)
        self.projectsMeetingsChecks_vbox.setObjectName(u"projectsMeetingsChecks_vbox")
        self.lblMeetingsProjectsHint = QLabel(self.scrollProjectsMeetingsContents)
        self.lblMeetingsProjectsHint.setObjectName(u"lblMeetingsProjectsHint")

        self.projectsMeetingsChecks_vbox.addWidget(self.lblMeetingsProjectsHint)

        self.sp_meet_proj = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.projectsMeetingsChecks_vbox.addItem(self.sp_meet_proj)

        self.scrollProjectsMeetings.setWidget(self.scrollProjectsMeetingsContents)

        self.boxMeetingsFilters_hbox.addWidget(self.scrollProjectsMeetings)

        self.sp_meet_mid = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.boxMeetingsFilters_hbox.addItem(self.sp_meet_mid)

        self.meetings_actions_hbox = QHBoxLayout()
        self.meetings_actions_hbox.setObjectName(u"meetings_actions_hbox")
        self.leMeetingSearch = QLineEdit(self.boxMeetingsFilters)
        self.leMeetingSearch.setObjectName(u"leMeetingSearch")

        self.meetings_actions_hbox.addWidget(self.leMeetingSearch)

        self.btnMeetingsApply = QPushButton(self.boxMeetingsFilters)
        self.btnMeetingsApply.setObjectName(u"btnMeetingsApply")

        self.meetings_actions_hbox.addWidget(self.btnMeetingsApply)

        self.sp_meet_act = QSpacerItem(16, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.meetings_actions_hbox.addItem(self.sp_meet_act)

        self.btnMeetingNew = QPushButton(self.boxMeetingsFilters)
        self.btnMeetingNew.setObjectName(u"btnMeetingNew")

        self.meetings_actions_hbox.addWidget(self.btnMeetingNew)

        self.btnMeetingEdit = QPushButton(self.boxMeetingsFilters)
        self.btnMeetingEdit.setObjectName(u"btnMeetingEdit")

        self.meetings_actions_hbox.addWidget(self.btnMeetingEdit)

        self.btnMeetingArchive = QPushButton(self.boxMeetingsFilters)
        self.btnMeetingArchive.setObjectName(u"btnMeetingArchive")

        self.meetings_actions_hbox.addWidget(self.btnMeetingArchive)


        self.boxMeetingsFilters_hbox.addLayout(self.meetings_actions_hbox)


        self.pageMeetings_vbox.addWidget(self.boxMeetingsFilters)

        self.boxAllMeetings = QGroupBox(self.pageMeetings)
        self.boxAllMeetings.setObjectName(u"boxAllMeetings")
        self.boxAllMeetings_vbox = QVBoxLayout(self.boxAllMeetings)
        self.boxAllMeetings_vbox.setObjectName(u"boxAllMeetings_vbox")
        self.tableMeetings = QTableWidget(self.boxAllMeetings)
        if (self.tableMeetings.columnCount() < 7):
            self.tableMeetings.setColumnCount(7)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.tableMeetings.setHorizontalHeaderItem(0, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.tableMeetings.setHorizontalHeaderItem(1, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.tableMeetings.setHorizontalHeaderItem(2, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.tableMeetings.setHorizontalHeaderItem(3, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        self.tableMeetings.setHorizontalHeaderItem(4, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        self.tableMeetings.setHorizontalHeaderItem(5, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        self.tableMeetings.setHorizontalHeaderItem(6, __qtablewidgetitem26)
        self.tableMeetings.setObjectName(u"tableMeetings")
        self.tableMeetings.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableMeetings.setAlternatingRowColors(True)
        self.tableMeetings.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tableMeetings.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableMeetings.setSortingEnabled(True)
        self.tableMeetings.horizontalHeader().setDefaultSectionSize(110)
        self.tableMeetings.horizontalHeader().setStretchLastSection(True)

        self.boxAllMeetings_vbox.addWidget(self.tableMeetings)


        self.pageMeetings_vbox.addWidget(self.boxAllMeetings)

        self.pageMeetings_vbox.setStretch(1, 1)
        self.mainStack.addWidget(self.pageMeetings)
        self.pageQuestions = QWidget()
        self.pageQuestions.setObjectName(u"pageQuestions")
        self.q_page_vbox = QVBoxLayout(self.pageQuestions)
        self.q_page_vbox.setObjectName(u"q_page_vbox")
        self.q_top_bar = QHBoxLayout()
        self.q_top_bar.setObjectName(u"q_top_bar")
        self.gbQSummary = QGroupBox(self.pageQuestions)
        self.gbQSummary.setObjectName(u"gbQSummary")
        self.q_sum_vbox = QVBoxLayout(self.gbQSummary)
        self.q_sum_vbox.setObjectName(u"q_sum_vbox")
        self.lblQOpen = QLabel(self.gbQSummary)
        self.lblQOpen.setObjectName(u"lblQOpen")

        self.q_sum_vbox.addWidget(self.lblQOpen)

        self.lblQClosedWeek = QLabel(self.gbQSummary)
        self.lblQClosedWeek.setObjectName(u"lblQClosedWeek")

        self.q_sum_vbox.addWidget(self.lblQClosedWeek)


        self.q_top_bar.addWidget(self.gbQSummary)

        self.gbQChart = QGroupBox(self.pageQuestions)
        self.gbQChart.setObjectName(u"gbQChart")
        self.q_chart_vbox = QVBoxLayout(self.gbQChart)
        self.q_chart_vbox.setObjectName(u"q_chart_vbox")
        self.q_chart_placeholder = QWidget(self.gbQChart)
        self.q_chart_placeholder.setObjectName(u"q_chart_placeholder")
        self.q_chart_placeholder.setMinimumSize(QSize(200, 60))

        self.q_chart_vbox.addWidget(self.q_chart_placeholder)


        self.q_top_bar.addWidget(self.gbQChart)


        self.q_page_vbox.addLayout(self.q_top_bar)

        self.q_actions_bar = QHBoxLayout()
        self.q_actions_bar.setObjectName(u"q_actions_bar")
        self.lblQAll = QLabel(self.pageQuestions)
        self.lblQAll.setObjectName(u"lblQAll")

        self.q_actions_bar.addWidget(self.lblQAll)

        self.q_actions_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.q_actions_bar.addItem(self.q_actions_spacer)

        self.btnQNew = QPushButton(self.pageQuestions)
        self.btnQNew.setObjectName(u"btnQNew")

        self.q_actions_bar.addWidget(self.btnQNew)

        self.btnQClose = QPushButton(self.pageQuestions)
        self.btnQClose.setObjectName(u"btnQClose")

        self.q_actions_bar.addWidget(self.btnQClose)

        self.btnQJumpToTask = QPushButton(self.pageQuestions)
        self.btnQJumpToTask.setObjectName(u"btnQJumpToTask")

        self.q_actions_bar.addWidget(self.btnQJumpToTask)


        self.q_page_vbox.addLayout(self.q_actions_bar)

        self.tableQuestions = QTableWidget(self.pageQuestions)
        if (self.tableQuestions.columnCount() < 4):
            self.tableQuestions.setColumnCount(4)
        __qtablewidgetitem27 = QTableWidgetItem()
        self.tableQuestions.setHorizontalHeaderItem(0, __qtablewidgetitem27)
        __qtablewidgetitem28 = QTableWidgetItem()
        self.tableQuestions.setHorizontalHeaderItem(1, __qtablewidgetitem28)
        __qtablewidgetitem29 = QTableWidgetItem()
        self.tableQuestions.setHorizontalHeaderItem(2, __qtablewidgetitem29)
        __qtablewidgetitem30 = QTableWidgetItem()
        self.tableQuestions.setHorizontalHeaderItem(3, __qtablewidgetitem30)
        self.tableQuestions.setObjectName(u"tableQuestions")
        self.tableQuestions.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableQuestions.setAlternatingRowColors(True)
        self.tableQuestions.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tableQuestions.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableQuestions.setWordWrap(False)
        self.tableQuestions.setRowCount(0)
        self.tableQuestions.setColumnCount(4)
        self.tableQuestions.horizontalHeader().setCascadingSectionResizes(False)
        self.tableQuestions.horizontalHeader().setMinimumSectionSize(40)
        self.tableQuestions.horizontalHeader().setDefaultSectionSize(120)
        self.tableQuestions.horizontalHeader().setStretchLastSection(True)
        self.tableQuestions.verticalHeader().setVisible(False)

        self.q_page_vbox.addWidget(self.tableQuestions)

        self.mainStack.addWidget(self.pageQuestions)

        self.content_vbox.addWidget(self.mainStack)

        self.body_splitter.addWidget(self.content)

        self.main_vbox.addWidget(self.body_splitter)

        self.main_vbox.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1301, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.mainStack.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Heartli OfficeTool", None))
        self.lblTitle.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.leSearch.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Suche\u2026", None))
        self.btnNavHome.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.btnNavTasks.setText(QCoreApplication.translate("MainWindow", u"Tasks", None))
        self.btnNavMeetings.setText(QCoreApplication.translate("MainWindow", u"Meetings", None))
        self.btnNavQuestions.setText(QCoreApplication.translate("MainWindow", u"Questions", None))
        self.btnNavFiles.setText(QCoreApplication.translate("MainWindow", u"Files", None))
        self.boxStats.setTitle(QCoreApplication.translate("MainWindow", u"\u00dcbersicht", None))
        self.lblOpenCount.setText(QCoreApplication.translate("MainWindow", u"Offene Aufgaben: 0", None))
        self.lblArchivedWeek.setText(QCoreApplication.translate("MainWindow", u"Archiv diese Woche: 0", None))
        self.boxUrgency.setTitle(QCoreApplication.translate("MainWindow", u"Anteile nach Dringlichkeit", None))
        self.boxDueToday.setTitle(QCoreApplication.translate("MainWindow", u"Heute f\u00e4llig", None))
        ___qtablewidgetitem = self.tableDueToday.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"ID", None));
        ___qtablewidgetitem1 = self.tableDueToday.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Beschreibung", None));
        ___qtablewidgetitem2 = self.tableDueToday.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Projekt", None));
        ___qtablewidgetitem3 = self.tableDueToday.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Status", None));
        ___qtablewidgetitem4 = self.tableDueToday.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Prio", None));
        ___qtablewidgetitem5 = self.tableDueToday.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"F\u00e4llig", None));
        self.boxFilesFilters.setTitle(QCoreApplication.translate("MainWindow", u"Filter & Aktionen", None))
        self.labelProject.setText(QCoreApplication.translate("MainWindow", u"Projekt:", None))
        self.cbFilesProject.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Projekt w\u00e4hlen\u2026", None))
        self.labelSuche.setText(QCoreApplication.translate("MainWindow", u"Suche:", None))
        self.btnFilesApply.setText(QCoreApplication.translate("MainWindow", u"Anwenden", None))
        self.btnFileNew.setText(QCoreApplication.translate("MainWindow", u"Neu", None))
        self.btnFileEdit.setText(QCoreApplication.translate("MainWindow", u"\u00d6ffnen/Bearbeiten", None))
        ___qtablewidgetitem6 = self.tableFiles.horizontalHeaderItem(0)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Name", None));
        ___qtablewidgetitem7 = self.tableFiles.horizontalHeaderItem(1)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Nummer/Pfad", None));
        ___qtablewidgetitem8 = self.tableFiles.horizontalHeaderItem(2)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Projekt", None));
        ___qtablewidgetitem9 = self.tableFiles.horizontalHeaderItem(3)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"Links IN", None));
        ___qtablewidgetitem10 = self.tableFiles.horizontalHeaderItem(4)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"Links OUT", None));
        ___qtablewidgetitem11 = self.tableFiles.horizontalHeaderItem(5)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"Notizen", None));
        ___qtablewidgetitem12 = self.tableFiles.horizontalHeaderItem(6)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"Typ", None));
        ___qtablewidgetitem13 = self.tableFiles.horizontalHeaderItem(7)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"Erstellt", None));
        self.boxTasksStats.setTitle(QCoreApplication.translate("MainWindow", u"\u00dcbersicht Tasks", None))
        self.lblOpenCountTasks.setText(QCoreApplication.translate("MainWindow", u"Offene Aufgaben: 0", None))
        self.lblArchivedWeekTasks.setText(QCoreApplication.translate("MainWindow", u"Archiv diese Woche: 0", None))
        self.boxUrgencyTasks.setTitle(QCoreApplication.translate("MainWindow", u"Anteile nach Dringlichkeit", None))
        self.boxTasksFilters.setTitle(QCoreApplication.translate("MainWindow", u"Filter & Aktionen", None))
        self.lblProjectsHint.setText(QCoreApplication.translate("MainWindow", u"Projekte (H\u00e4kchen = anzeigen)", None))
        self.leTaskSearch.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Suche\u2026", None))
        self.btnTasksApply.setText(QCoreApplication.translate("MainWindow", u"Anwenden", None))
        self.btnTaskNew.setText(QCoreApplication.translate("MainWindow", u"Neu", None))
        self.btnTaskEdit.setText(QCoreApplication.translate("MainWindow", u"\u00d6ffnen/Bearbeiten", None))
        self.btnTaskArchive.setText(QCoreApplication.translate("MainWindow", u"Archiv", None))
        self.boxAllTasks.setTitle(QCoreApplication.translate("MainWindow", u"Alle Tasks", None))
        ___qtablewidgetitem14 = self.tableAllTasks.horizontalHeaderItem(0)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"ID", None));
        ___qtablewidgetitem15 = self.tableAllTasks.horizontalHeaderItem(1)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"Beschreibung", None));
        ___qtablewidgetitem16 = self.tableAllTasks.horizontalHeaderItem(2)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"Projekt", None));
        ___qtablewidgetitem17 = self.tableAllTasks.horizontalHeaderItem(3)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"Status", None));
        ___qtablewidgetitem18 = self.tableAllTasks.horizontalHeaderItem(4)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"Prio", None));
        ___qtablewidgetitem19 = self.tableAllTasks.horizontalHeaderItem(5)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"F\u00e4llig", None));
        self.boxMeetingsFilters.setTitle(QCoreApplication.translate("MainWindow", u"Filter & Aktionen", None))
        self.lblMeetingsProjectsHint.setText(QCoreApplication.translate("MainWindow", u"Projekte (H\u00e4kchen = anzeigen)", None))
        self.leMeetingSearch.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Suche\u2026 (Titel/Notizen)", None))
        self.btnMeetingsApply.setText(QCoreApplication.translate("MainWindow", u"Anwenden", None))
        self.btnMeetingNew.setText(QCoreApplication.translate("MainWindow", u"Neu", None))
        self.btnMeetingEdit.setText(QCoreApplication.translate("MainWindow", u"\u00d6ffnen/Bearbeiten", None))
        self.btnMeetingArchive.setText(QCoreApplication.translate("MainWindow", u"Archiv", None))
        self.boxAllMeetings.setTitle(QCoreApplication.translate("MainWindow", u"Meetings", None))
        ___qtablewidgetitem20 = self.tableMeetings.horizontalHeaderItem(0)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("MainWindow", u"Datum", None));
        ___qtablewidgetitem21 = self.tableMeetings.horizontalHeaderItem(1)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("MainWindow", u"Zeit", None));
        ___qtablewidgetitem22 = self.tableMeetings.horizontalHeaderItem(2)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("MainWindow", u"Titel", None));
        ___qtablewidgetitem23 = self.tableMeetings.horizontalHeaderItem(3)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("MainWindow", u"Projekt", None));
        ___qtablewidgetitem24 = self.tableMeetings.horizontalHeaderItem(4)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("MainWindow", u"Ort", None));
        ___qtablewidgetitem25 = self.tableMeetings.horizontalHeaderItem(5)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("MainWindow", u"Aufgaben#", None));
        ___qtablewidgetitem26 = self.tableMeetings.horizontalHeaderItem(6)
        ___qtablewidgetitem26.setText(QCoreApplication.translate("MainWindow", u"Notizen", None));
        self.gbQSummary.setTitle(QCoreApplication.translate("MainWindow", u"\u00dcbersicht Fragen", None))
        self.lblQOpen.setText(QCoreApplication.translate("MainWindow", u"Offene Fragen: 0", None))
        self.lblQClosedWeek.setText(QCoreApplication.translate("MainWindow", u"Geschlossen diese Woche: 0", None))
        self.gbQChart.setTitle(QCoreApplication.translate("MainWindow", u"Anteile nach Typ", None))
        self.lblQAll.setText(QCoreApplication.translate("MainWindow", u"Alle Fragen", None))
        self.btnQNew.setText(QCoreApplication.translate("MainWindow", u"Neue Frage", None))
        self.btnQClose.setText(QCoreApplication.translate("MainWindow", u"Abschliessen", None))
        self.btnQJumpToTask.setText(QCoreApplication.translate("MainWindow", u"Zur Aufgabe springen", None))
        ___qtablewidgetitem27 = self.tableQuestions.horizontalHeaderItem(0)
        ___qtablewidgetitem27.setText(QCoreApplication.translate("MainWindow", u"Person", None));
        ___qtablewidgetitem28 = self.tableQuestions.horizontalHeaderItem(1)
        ___qtablewidgetitem28.setText(QCoreApplication.translate("MainWindow", u"Frage", None));
        ___qtablewidgetitem29 = self.tableQuestions.horizontalHeaderItem(2)
        ___qtablewidgetitem29.setText(QCoreApplication.translate("MainWindow", u"Status", None));
        ___qtablewidgetitem30 = self.tableQuestions.horizontalHeaderItem(3)
        ___qtablewidgetitem30.setText(QCoreApplication.translate("MainWindow", u"Typ", None));
    # retranslateUi

