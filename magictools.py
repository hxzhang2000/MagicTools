# Form implementation generated from reading ui file 'C:\hxzhang\sourcecode\python\MagicTools\mainwindow.ui'
#
# Created by: PyQt6 UI code generator 6.1.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.TasktableView = QtWidgets.QTableView(self.centralwidget)
        self.TasktableView.setObjectName("TasktableView")
        self.gridLayout.addWidget(self.TasktableView, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menuTask = QtWidgets.QMenu(self.menubar)
        self.menuTask.setObjectName("menuTask")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionAdd = QtGui.QAction(MainWindow)
        self.actionAdd.setObjectName("actionAdd")
        self.actionDel = QtGui.QAction(MainWindow)
        self.actionDel.setObjectName("actionDel")
        self.actionEdit = QtGui.QAction(MainWindow)
        self.actionEdit.setObjectName("actionEdit")
        self.actionRefash = QtGui.QAction(MainWindow)
        self.actionRefash.setObjectName("actionRefash")
        self.actionSaveAs = QtGui.QAction(MainWindow)
        self.actionSaveAs.setObjectName("actionSaveAs")
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionNew = QtGui.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionClear = QtGui.QAction(MainWindow)
        self.actionClear.setObjectName("actionClear")
        self.actionRun = QtGui.QAction(MainWindow)
        self.actionRun.setObjectName("actionRun")
        self.menu.addAction(self.actionNew)
        self.menu.addSeparator()
        self.menu.addAction(self.actionOpen)
        self.menu.addAction(self.actionSaveAs)
        self.menu.addSeparator()
        self.menu.addAction(self.actionExit)
        self.menuTask.addAction(self.actionRun)
        self.menuTask.addSeparator()
        self.menuTask.addAction(self.actionAdd)
        self.menuTask.addAction(self.actionDel)
        self.menuTask.addAction(self.actionEdit)
        self.menuTask.addSeparator()
        self.menuTask.addAction(self.actionClear)
        self.menuTask.addAction(self.actionRefash)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menuTask.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MagicTools"))
        self.menu.setTitle(_translate("MainWindow", "File"))
        self.menuTask.setTitle(_translate("MainWindow", "Task"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionAdd.setText(_translate("MainWindow", "Add"))
        self.actionDel.setText(_translate("MainWindow", "Del"))
        self.actionEdit.setText(_translate("MainWindow", "Edit"))
        self.actionRefash.setText(_translate("MainWindow", "Refresh"))
        self.actionSaveAs.setText(_translate("MainWindow", "SaveAs"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionClear.setText(_translate("MainWindow", "Clear"))
        self.actionRun.setText(_translate("MainWindow", "Run"))
