# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'selectnamedlg.ui'
##
## Created by: Qt User Interface Compiler version 6.2.0
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QHeaderView, QSizePolicy, QTableView)

class Ui_SelectNameDialog(object):
    def setupUi(self, SelectNameDialog):
        if not SelectNameDialog.objectName():
            SelectNameDialog.setObjectName(u"SelectNameDialog")
        SelectNameDialog.resize(400, 300)
        self.buttonBox = QDialogButtonBox(SelectNameDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(290, 20, 81, 241))
        self.buttonBox.setOrientation(Qt.Vertical)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.tableView = QTableView(SelectNameDialog)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setGeometry(QRect(0, 0, 281, 301))

        self.retranslateUi(SelectNameDialog)
        self.buttonBox.accepted.connect(SelectNameDialog.accept)
        self.buttonBox.rejected.connect(SelectNameDialog.reject)

        QMetaObject.connectSlotsByName(SelectNameDialog)
    # setupUi

    def retranslateUi(self, SelectNameDialog):
        SelectNameDialog.setWindowTitle(QCoreApplication.translate("SelectNameDialog", u"Dialog", None))
    # retranslateUi

