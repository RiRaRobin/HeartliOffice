# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'file_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFormLayout, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QTextEdit, QVBoxLayout, QWidget)

class Ui_FileDialog(object):
    def setupUi(self, FileDialog):
        if not FileDialog.objectName():
            FileDialog.setObjectName(u"FileDialog")
        FileDialog.resize(610, 949)
        self.vbox_outer = QVBoxLayout(FileDialog)
        self.vbox_outer.setSpacing(8)
        self.vbox_outer.setObjectName(u"vbox_outer")
        self.form = QFormLayout()
        self.form.setObjectName(u"form")
        self.form.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.lblDokName = QLabel(FileDialog)
        self.lblDokName.setObjectName(u"lblDokName")

        self.form.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lblDokName)

        self.leFileName = QLineEdit(FileDialog)
        self.leFileName.setObjectName(u"leFileName")

        self.form.setWidget(0, QFormLayout.ItemRole.FieldRole, self.leFileName)

        self.lblDokNrPfad = QLabel(FileDialog)
        self.lblDokNrPfad.setObjectName(u"lblDokNrPfad")

        self.form.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lblDokNrPfad)

        self.leFileRef = QLineEdit(FileDialog)
        self.leFileRef.setObjectName(u"leFileRef")

        self.form.setWidget(1, QFormLayout.ItemRole.FieldRole, self.leFileRef)

        self.lblProjekt = QLabel(FileDialog)
        self.lblProjekt.setObjectName(u"lblProjekt")

        self.form.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lblProjekt)

        self.leFileProject = QLineEdit(FileDialog)
        self.leFileProject.setObjectName(u"leFileProject")

        self.form.setWidget(2, QFormLayout.ItemRole.FieldRole, self.leFileProject)

        self.lblBeschreibung = QLabel(FileDialog)
        self.lblBeschreibung.setObjectName(u"lblBeschreibung")

        self.form.setWidget(3, QFormLayout.ItemRole.LabelRole, self.lblBeschreibung)

        self.teFileDescription = QTextEdit(FileDialog)
        self.teFileDescription.setObjectName(u"teFileDescription")
        self.teFileDescription.setEnabled(True)

        self.form.setWidget(3, QFormLayout.ItemRole.FieldRole, self.teFileDescription)

        self.lblStatus = QLabel(FileDialog)
        self.lblStatus.setObjectName(u"lblStatus")

        self.form.setWidget(4, QFormLayout.ItemRole.LabelRole, self.lblStatus)

        self.cbFileType = QComboBox(FileDialog)
        self.cbFileType.setObjectName(u"cbFileType")

        self.form.setWidget(4, QFormLayout.ItemRole.FieldRole, self.cbFileType)

        self.lblNotizen = QLabel(FileDialog)
        self.lblNotizen.setObjectName(u"lblNotizen")

        self.form.setWidget(5, QFormLayout.ItemRole.LabelRole, self.lblNotizen)

        self.teFileNotes = QTextEdit(FileDialog)
        self.teFileNotes.setObjectName(u"teFileNotes")

        self.form.setWidget(5, QFormLayout.ItemRole.FieldRole, self.teFileNotes)

        self.lblFollow = QLabel(FileDialog)
        self.lblFollow.setObjectName(u"lblFollow")

        self.form.setWidget(6, QFormLayout.ItemRole.LabelRole, self.lblFollow)

        self.leFileTags = QTextEdit(FileDialog)
        self.leFileTags.setObjectName(u"leFileTags")

        self.form.setWidget(6, QFormLayout.ItemRole.FieldRole, self.leFileTags)

        self.leLinksInInput = QLineEdit(FileDialog)
        self.leLinksInInput.setObjectName(u"leLinksInInput")

        self.form.setWidget(7, QFormLayout.ItemRole.FieldRole, self.leLinksInInput)

        self.leLinksOutInput = QLineEdit(FileDialog)
        self.leLinksOutInput.setObjectName(u"leLinksOutInput")

        self.form.setWidget(10, QFormLayout.ItemRole.FieldRole, self.leLinksOutInput)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.btnAddLinkIn = QPushButton(FileDialog)
        self.btnAddLinkIn.setObjectName(u"btnAddLinkIn")

        self.horizontalLayout_2.addWidget(self.btnAddLinkIn)

        self.btnRemoveLinkIn = QPushButton(FileDialog)
        self.btnRemoveLinkIn.setObjectName(u"btnRemoveLinkIn")

        self.horizontalLayout_2.addWidget(self.btnRemoveLinkIn)


        self.form.setLayout(8, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_2)

        self.label = QLabel(FileDialog)
        self.label.setObjectName(u"label")

        self.form.setWidget(7, QFormLayout.ItemRole.LabelRole, self.label)

        self.label_2 = QLabel(FileDialog)
        self.label_2.setObjectName(u"label_2")

        self.form.setWidget(10, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.btnAddLinkOut = QPushButton(FileDialog)
        self.btnAddLinkOut.setObjectName(u"btnAddLinkOut")

        self.horizontalLayout_3.addWidget(self.btnAddLinkOut)

        self.btnRemoveLinkOut = QPushButton(FileDialog)
        self.btnRemoveLinkOut.setObjectName(u"btnRemoveLinkOut")

        self.horizontalLayout_3.addWidget(self.btnRemoveLinkOut)


        self.form.setLayout(11, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_3)

        self.listFileLinksIn = QListWidget(FileDialog)
        self.listFileLinksIn.setObjectName(u"listFileLinksIn")

        self.form.setWidget(9, QFormLayout.ItemRole.FieldRole, self.listFileLinksIn)

        self.listFileLinksOut = QListWidget(FileDialog)
        self.listFileLinksOut.setObjectName(u"listFileLinksOut")

        self.form.setWidget(12, QFormLayout.ItemRole.FieldRole, self.listFileLinksOut)


        self.vbox_outer.addLayout(self.form)

        self.buttonBox = QDialogButtonBox(FileDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Save)

        self.vbox_outer.addWidget(self.buttonBox)


        self.retranslateUi(FileDialog)

        QMetaObject.connectSlotsByName(FileDialog)
    # setupUi

    def retranslateUi(self, FileDialog):
        FileDialog.setWindowTitle(QCoreApplication.translate("FileDialog", u"Neue Aufgabe", None))
        self.lblDokName.setText(QCoreApplication.translate("FileDialog", u"Dokument-Name", None))
        self.lblDokNrPfad.setText(QCoreApplication.translate("FileDialog", u"Dokument-Nr/Pfad", None))
        self.lblProjekt.setText(QCoreApplication.translate("FileDialog", u"Projekt", None))
        self.lblBeschreibung.setText(QCoreApplication.translate("FileDialog", u"Beschreibung", None))
        self.lblStatus.setText(QCoreApplication.translate("FileDialog", u"Typ", None))
        self.lblNotizen.setText(QCoreApplication.translate("FileDialog", u"Notizen", None))
        self.lblFollow.setText(QCoreApplication.translate("FileDialog", u"Tags", None))
        self.btnAddLinkIn.setText(QCoreApplication.translate("FileDialog", u"Hinzuf\u00fcgen", None))
        self.btnRemoveLinkIn.setText(QCoreApplication.translate("FileDialog", u"Entfernen", None))
        self.label.setText(QCoreApplication.translate("FileDialog", u"Abh\u00e4ngig nach oben", None))
        self.label_2.setText(QCoreApplication.translate("FileDialog", u"Abh\u00e4ngigkeit nach unten", None))
        self.btnAddLinkOut.setText(QCoreApplication.translate("FileDialog", u"Hinzuf\u00fcgen", None))
        self.btnRemoveLinkOut.setText(QCoreApplication.translate("FileDialog", u"Entfernen", None))
    # retranslateUi

