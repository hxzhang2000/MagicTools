# coding = utf-8

import sys
#from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QApplication, QMainWindow, QAbstractItemView, QTableView, QHeaderView, QDialog
#from PyQt6.QtCore import QModelIndex
import magictools
import selectnamedlg
from functools import partial
import const 
from task_mdgraph import task_mdgraph
from task_classifypic import task_classifypic
from task_planewar import task_planewar
from task_bookgraph import task_bookgraph
from task_mappic import task_mappic

const.MODEL_LIST = [[const.BOOKGRAPH_NAME,'tools'],
    [const.CLASSIFYPIC_NAME,'tools'],
    [const.MDGRAPH_NAME,'tools'],
    [const.MAPPIC_NAME,'tools'],
    [const.PLANEWAR_NAME,'game']]
const.ITEM_NAME = 'name'
const.ITEM_PARAM = 'parameter'
const.ITEM_POINT = 'item'

class cTaskManager:

    tasks = []
    '''
    name : ''
    type : ''
    parameter : json
    item : taskinterface object
    '''

    def cfInitModel(self) -> None:
        self.tasks.clear()

    def cfRunItem(self,index: int) -> int:
        if index < 0 or index >= len(self.tasks):
            return -1
        
        d = self.tasks[index]
        item = d.get(const.ITEM_POINT)
        if item == None:
            return -1
        
        return item.run()

    def cfAddItem(self,name: str, parameter: str) -> int:
        d = dict()

        d[const.ITEM_NAME] = name
        d[const.ITEM_PARAM] = parameter 

        if name == const.MDGRAPH_NAME:
            item = task_mdgraph()
            d[const.ITEM_POINT] = item
            
            if len(parameter) > 0:
                item.setparameter(parameter)
        elif name == const.CLASSIFYPIC_NAME:
            item = task_classifypic()
            d[const.ITEM_POINT] = item
            
            if len(parameter) > 0:
                item.setparameter(parameter)
        elif name == const.PLANEWAR_NAME:
            item = task_planewar()
            d[const.ITEM_POINT] = item
            
            if len(parameter) > 0:
                item.setparameter(parameter)
        elif name == const.BOOKGRAPH_NAME:
            item = task_bookgraph()
            d[const.ITEM_POINT] = item
            
            if len(parameter) > 0:
                item.setparameter(parameter)
        elif name == const.MAPPIC_NAME:
            item  = task_mappic()
            d[const.ITEM_POINT] = item
            
            if len(parameter) > 0:
                item.setparameter(parameter)
        else:
            d[const.ITEM_POINT] = None

        self.tasks.append(d)
        return len(self.tasks)

    def cfDelItem(self,index: int) -> None:
        if index < 0 or len(self.tasks) <= index:
            return
        self.tasks.pop(index)

    def cfClear(self) -> None:
        self.tasks.clear()

    def cfEditItem(self,index: int, parameter: str) -> int:
        if index < 0 or len(self.tasks) <= index:
            return -1
        
        d : dict
        d = self.tasks[index]
        
        item = d.get(const.ITEM_POINT)
        if item == None:
            return -1
        
        ret = item.setparameter(parameter)
        if ret != 0:
            return ret
        
        ret = item.opensetup()
        if ret != 0:
            return ret

        parameter = item.getparameter()
        d.setdefault(const.ITEM_PARAM, parameter)
        return ret
    
    def cfGetParameter(self, index: int) -> str:
        
        if index < 0 or len(self.tasks) <= index:
            return -1
        
        d : dict
        d = self.tasks[index]
        
        return d.get(const.ITEM_PARAM)


class QMyDialog(QDialog):

    model = QStandardItemModel() 
    name = ''
    itemtype = ''

    def __init__(self):
        self.model.setHorizontalHeaderLabels(['type','name'])

        for itemlist in const.MODEL_LIST:
            self.model.appendRow([QStandardItem(itemlist[1]),QStandardItem(itemlist[0])])

        super().__init__()

    def cfUpdateName(self,ui: selectnamedlg.Ui_SelectNameDialog) -> None:
        #QModelIndex
        #indexs = self.tableView.selectionModel().selection().indexes()#返回结果是QModelIndex类对象，里面有row和column方法获取行列索引
        #index = indexs[0].row()

        irow = ui.tableView.currentIndex().row()
        icolumn = 1

        item = self.model.item(irow,icolumn)
        self.name = item.text()
        
        icolumn = 0
        item = self.model.item(irow, icolumn)
        self.itemtype = item.text()

    def cfOnClose(self) -> None:
        self.model.clear()


class QMyMainWindow(QMainWindow, cTaskManager):

    model = QStandardItemModel()

    def cfInitModel(self) -> None:
        self.model.setHorizontalHeaderLabels(['type','name','status'])
        super().cfInitModel()

    def cfRunItem(self,index: int) -> int:
        item = QStandardItem('')
        self.model.setItem(index, 2, item)

        ret = super().cfRunItem(index)
        
        #更新状态
        status = 'successed'
        if ret != 0:
            status = 'errror ret=' + str(ret)

        item = QStandardItem(status)
        self.model.setItem(index, 2, item)
        
        return ret

    def cfOnAccept(self) -> None:
        #QMessageBox.information(self,'info','aaaa')
        pass
        

    def cfAddItem(self) -> int:
        parameter = ''
        index = -1

        ui = selectnamedlg.Ui_SelectNameDialog()
        dlg = QMyDialog()
        ui.setupUi(dlg)

        ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)#所有列自动拉伸，充满界面
        ui.tableView.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)#设置只能选中一行
        ui.tableView.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)#不可编辑
        ui.tableView.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows);#设置只有行选中

        ui.buttonBox.accepted.connect(self.cfOnAccept)

        ui.tableView.setModel(dlg.model)
        if dlg.exec():
            dlg.cfUpdateName(ui)

            self.model.appendRow([QStandardItem(dlg.itemtype),
                QStandardItem(dlg.name),
                QStandardItem('-')])

            index = super().cfAddItem(dlg.name,parameter)
            
            ui.tableView.selectRow(index)

        dlg.cfOnClose()

        return index


    def cfDelItem(self,index: int) -> None:

        self.model.removeRow(index)
        super().cfDelItem(index)

    def cfClear(self) -> None:
        self.model.removeRows(0,self.rowCount())
        super().cfClear()

    def cfEditItem(self,index: int) -> None:
        parameter = super().cfGetParameter(index)

        super().cfEditItem(index, parameter)

    def cfNew(self) -> None:
        self.cfClear()

    def cfOpen(self) -> None:
        filename = ''

        self.model.cfOpen(filename)

    def cfSaveAs(self) -> None:
        filename = ''

        self.model.cfSaveAs(filename)

    def cfRefash(self) -> None:
        pass


def fMenuFileExit(ui:magictools.Ui_MainWindow, MainWindow: QMyMainWindow) -> None:
    sys.exit()

def fMenuFileNew(ui:magictools.Ui_MainWindow, MainWindow: QMyMainWindow) -> None:
    MainWindow.cfNew()

def fMenuFileOpen(ui:magictools.Ui_MainWindow, MainWindow: QMyMainWindow) -> None:
    MainWindow.cfOpen()

def fMenuFileSaveAs(ui:magictools.Ui_MainWindow, MainWindow: QMyMainWindow) -> None:
    MainWindow.cfSaveAs()

def fMenuTaskRun(ui:magictools.Ui_MainWindow, MainWindow: QMyMainWindow) -> None:

    indexs = ui.TasktableView.selectionModel().selection().indexes()#返回结果是QModelIndex类对象，里面有row和column方法获取行列索引
    index = indexs[0].row()

    MainWindow.cfRunItem(index)
        
def fMenuTaskAdd(ui:magictools.Ui_MainWindow, MainWindow: QMyMainWindow) -> None:
    MainWindow.cfAddItem()

def fMenuTaskDel(ui:magictools.Ui_MainWindow, MainWindow: QMyMainWindow) -> None:
    indexs = ui.TasktableView.selectionModel().selection().indexes()#返回结果是QModelIndex类对象，里面有row和column方法获取行列索引
    index = indexs[0].row()

    MainWindow.cfDelItem(index)

def fMenuTaskEdit(ui:magictools.Ui_MainWindow, MainWindow: QMyMainWindow) -> None:
    indexs = ui.TasktableView.selectionModel().selection().indexes()#返回结果是QModelIndex类对象，里面有row和column方法获取行列索引
    index = indexs[0].row()

    MainWindow.cfEditItem(index)

def fMenuTaskClear(ui:magictools.Ui_MainWindow, MainWindow: QMyMainWindow) -> None:
    MainWindow.cfClear()

def fMenuTaskRefash(ui:magictools.Ui_MainWindow, MainWindow: QMyMainWindow) -> None:
    MainWindow.cfRefash()

def fMainWindowInit(ui:magictools.Ui_MainWindow, MainWindow: QMyMainWindow) -> None:

    MainWindow.cfInitModel()

    #ui.TasktableView.horizontalHeader().setStretchLastSection(True)#最后一列决定充满剩下的界面
    ui.TasktableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)#所有列自动拉伸，充满界面
    ui.TasktableView.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)#设置只能选中一行
    ui.TasktableView.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)#不可编辑
    ui.TasktableView.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows);#设置只有行选中
    ui.TasktableView.setModel(MainWindow.model)

    MainWindow.cfRefash()


def main() -> None:
    app = QApplication(sys.argv)
    MainWindow = QMyMainWindow()
    ui = magictools.Ui_MainWindow()
    ui.setupUi(MainWindow)

    #注册事件
    ui.actionExit.triggered.connect(partial(fMenuFileExit,ui, MainWindow))
    ui.actionNew.triggered.connect(partial(fMenuFileNew,ui, MainWindow))
    ui.actionOpen.triggered.connect(partial(fMenuFileOpen,ui, MainWindow))
    ui.actionSaveAs.triggered.connect(partial(fMenuFileSaveAs,ui, MainWindow))
    ui.actionRun.triggered.connect(partial(fMenuTaskRun,ui,MainWindow))
    ui.actionAdd.triggered.connect(partial(fMenuTaskAdd,ui,MainWindow))
    ui.actionDel.triggered.connect(partial(fMenuTaskDel,ui,MainWindow))
    ui.actionEdit.triggered.connect(partial(fMenuTaskEdit,ui,MainWindow))
    ui.actionClear.triggered.connect(partial(fMenuTaskClear,ui,MainWindow))
    ui.actionRefash.triggered.connect(partial(fMenuTaskRefash,ui,MainWindow))

    #初始化窗口
    fMainWindowInit(ui, MainWindow)
    

    MainWindow.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()


# cd C:\Users\hxzha\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\LocalCache\local-packages\Python39\Scripts
# pyuic6 -o C:\hxzhang\sourcecode\python\MagicTools\magictools.py C:\hxzhang\sourcecode\python\MagicTools\mainwindow.ui
# pyuic6 -o C:\hxzhang\sourcecode\python\MagicTools\selectnamedlg.py C:\hxzhang\sourcecode\python\MagicTools\selectnamedlg.ui
# pyuic6 -o C:\hxzhang\sourcecode\python\MagicTools\taskmdgraph_setup.py C:\hxzhang\sourcecode\python\MagicTools\taskmdgraph_setup.ui



