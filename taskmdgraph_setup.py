# Form implementation generated from reading ui file 'C:\hxzhang\sourcecode\python\MagicTools\taskmdgraph_setup.ui'
#
# Created by: PyQt6 UI code generator 6.1.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_taskmdgraph_Dialog(object):
    def setupUi(self, taskmdgraph_Dialog):
        taskmdgraph_Dialog.setObjectName("taskmdgraph_Dialog")
        taskmdgraph_Dialog.resize(536, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(taskmdgraph_Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(160, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.lineEdit_MDFile = QtWidgets.QLineEdit(taskmdgraph_Dialog)
        self.lineEdit_MDFile.setGeometry(QtCore.QRect(70, 30, 381, 20))
        self.lineEdit_MDFile.setObjectName("lineEdit_MDFile")
        self.lineEdit_SVGFile = QtWidgets.QLineEdit(taskmdgraph_Dialog)
        self.lineEdit_SVGFile.setGeometry(QtCore.QRect(70, 80, 381, 20))
        self.lineEdit_SVGFile.setObjectName("lineEdit_SVGFile")
        self.label = QtWidgets.QLabel(taskmdgraph_Dialog)
        self.label.setGeometry(QtCore.QRect(10, 30, 54, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(taskmdgraph_Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 80, 54, 16))
        self.label_2.setObjectName("label_2")
        self.pushButton_mdfile = QtWidgets.QPushButton(taskmdgraph_Dialog)
        self.pushButton_mdfile.setGeometry(QtCore.QRect(460, 30, 31, 24))
        self.pushButton_mdfile.setObjectName("pushButton_mdfile")
        self.pushButton_svgfile = QtWidgets.QPushButton(taskmdgraph_Dialog)
        self.pushButton_svgfile.setGeometry(QtCore.QRect(460, 80, 31, 24))
        self.pushButton_svgfile.setObjectName("pushButton_svgfile")
        self.label_3 = QtWidgets.QLabel(taskmdgraph_Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 140, 81, 16))
        self.label_3.setObjectName("label_3")
        self.lineEdit_tableindex = QtWidgets.QLineEdit(taskmdgraph_Dialog)
        self.lineEdit_tableindex.setGeometry(QtCore.QRect(110, 140, 113, 20))
        self.lineEdit_tableindex.setObjectName("lineEdit_tableindex")
        self.comboBox = QtWidgets.QComboBox(taskmdgraph_Dialog)
        self.comboBox.setGeometry(QtCore.QRect(110, 190, 111, 22))
        self.comboBox.setObjectName("comboBox")
        self.label_4 = QtWidgets.QLabel(taskmdgraph_Dialog)
        self.label_4.setGeometry(QtCore.QRect(10, 190, 81, 16))
        self.label_4.setObjectName("label_4")

        self.retranslateUi(taskmdgraph_Dialog)
        self.buttonBox.accepted.connect(taskmdgraph_Dialog.accept)
        self.buttonBox.rejected.connect(taskmdgraph_Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(taskmdgraph_Dialog)

    def retranslateUi(self, taskmdgraph_Dialog):
        _translate = QtCore.QCoreApplication.translate
        taskmdgraph_Dialog.setWindowTitle(_translate("taskmdgraph_Dialog", "mdgraph setup"))
        self.label.setText(_translate("taskmdgraph_Dialog", "MD File???"))
        self.label_2.setText(_translate("taskmdgraph_Dialog", "SVG File???"))
        self.pushButton_mdfile.setText(_translate("taskmdgraph_Dialog", "..."))
        self.pushButton_svgfile.setText(_translate("taskmdgraph_Dialog", "..."))
        self.label_3.setText(_translate("taskmdgraph_Dialog", "table index???"))
        self.label_4.setText(_translate("taskmdgraph_Dialog", "graph type???"))
