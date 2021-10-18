# coding = utf-8
from PyQt6.QtWidgets import QDialog, QFileDialog
from taskinterface import taskinterface
import markdown
import pandas as pd
#from pandas.core.base import NoNewAttributesMixin
import pygal                                                       # First import pygal
import const
import math
import json
import taskmdgraph_setup
import os
from functools import partial

const.TABLE_ALL = -1                            #处理md文件中的全部表格
const.GRAPH_LINE = 1                            #line图表
const.GRAPH_RANDAR = 2                          #pandar图表
const.MDGRAPH_NAME = 'markdown graph'

class task_mdgraph(taskinterface):

    def __init__(self) -> None:

        self._name = const.MDGRAPH_NAME
        self._tasktype = 'tools'
        self._parameter = ''

        self._mdFilename = 'C:\hxzhang\hxzhang\work\MyFiles\hxzhang知识库\减肥\减肥计划.md'
        self._svgFilename = 'C:\hxzhang\hxzhang\work\MyFiles\hxzhang知识库\减肥\减肥计划-table2.svg'
        self._catchtableIndex = 2       #const.TABLE_ALL
        self._graphtype = const.GRAPH_LINE

        super().__init__()


    def _fAnalyseTable(self, mdFilename: str) -> list:
        """分析md文件中表格信息，并以表格前最后一个标题（#）来作为表格标题

        Args:
            mdFilename (str): markdown文件全路径名称

        Returns:
            list: 分析后的表格列表，每个表格的md字符串
        """        

        #读取md文件
        with open(mdFilename, encoding= "utf-8") as f:
            lines = f.readlines()

        #判断空文件
        if len(lines) <= 0:
            return None

        #解析所有表格
        tables = []         #所有表格的列表
        table = ''
        title = ''
        intotable = False

        for line in lines:
            if line[0] == '#':
                #找表格前最后一个标题，作为表格的标题
                title = line.replace('#','').lstrip()
            elif line[0] == '|' :            #行首是'|'的，都认为是表格行
                intotable = True
                table += line              #只要是表格数据，就直接加入当前表格中
            else :
                if intotable:
                    # 刚刚从表格中出来
                    tables.append([title, table])        #加入表格列表中

                    #当前表格清零
                    table = ''

                intotable = False

        return tables

    def _fConverttoNone(self, dict: dict) -> dict:
        """
        # 1.处理'/'为none
        # 2.将字符串形式的数值，转换为float
        # 3.字典中排除非数字列

        Args:
            dict (dict): 传入的单个表格的字典数据

        Returns:
            dict: 处理完成的表格字典数据
        """        

        i = 0       #计数第一列

        dellist = []                #用于记录需要删除的key，无法转换为数字，无法绘图
        bDel = False
        # 遍历字典列表
        for key,values in  dict.items():

            bDel = False

            #判断是否第一列
            if i==0 :
                #第一列不做处理
                pass
            else :
                #只有数据才需要处理'/'为none
                vl = len(values)
                for vi in range(0,vl):
                    if values[vi] == '/':
                        values[vi] = None
                    else :
                        try:
                            values[vi] = float(values[vi])        #将原字符串字段内容，转换为数值，否则render会报错
                        except ValueError:
                            #走到这里，说明float报异常，传入的是字符串
                            bDel = True                            #记录这一列需要删除，不能直接删除，否则循环会报错
                        else:
                            #走到这里，说明没有异常，可能有两种情况，1）正常数值，2）nan，就是表格没填写内容
                            #表格未填写内容，获取到为nan，转换为none
                            if math.isnan(values[vi]):
                                values[vi] = None
                if bDel:
                    dellist.append(key)                         #记录要删除的key
                #已经自动更新临时字典内容

            i = i +1

        #删除所有无法转为数值的列
        for key in dellist:
            dict.pop(key)

        #print(dict)
        return dict

    def _fConvertTableToDict(self, table: str) -> dict:
        """单个表格的md字符串，转换为dict数据

        Args:
            table (str): 单个表格的md字符串

        Returns:
            dict: 转换后的dict
        """
        #表格转换为html格式
        hs = markdown.markdown(table,extensions=['markdown.extensions.toc','markdown.extensions.fenced_code','markdown.extensions.tables'])
        #解析为dataframe的lists
        dfname = pd.read_html(hs, encoding= "utf-8" )

        #判断空的list，可能没解析出来表格
        if len(dfname) <= 0:
            return None

        #判断空表格，没有数据行
        nrow = dfname[0].shape[0]
        if nrow <= 0:
            return None
        #只有一列没有数据
        ncol = dfname[0].shape[1]
        if ncol <= 1:
            return None

        return self._fConverttoNone(dfname[0].to_dict('list'))


    def _fDrawGraph_line(self, dict : dict,svgFilename: str,title: str) -> None:
        """画线条图，生成svg文件

        Args:
            dict (dict): 表格的dict
            svgFilename (str): 生成的svg全路径文件名
            title (str): 表格标题
        """
        #开始画图
        line_chart = pygal.Line(interpolate='cubic',dynamic_print_values=True)
        line_chart.title = title

        i = 0       #计数第一列
        # 遍历字典列表
        for key,values in  dict.items():

            #判断是否第一列，做为x轴数据
            if i==0 :
                line_chart.x_labels =  values
            else :
                line_chart.add(key, values)

            i = i+1

        line_chart.value_formatter = lambda x: "%f" % x
        line_chart.render_to_file(svgFilename) 

        return None

    def _fDrawGraph_Radar(self, dict: dict,svgFilename: str,title: str)->None:
        """画radar图，生成svg文件

        Args:
            dict (dict): 表格的dict
            svgFilename (str): 生成的svg全路径文件名
            title (str): 表格标题
        """

        #开始画图
        line_chart = pygal.Radar()
        line_chart.title = title

        i = 0       #计数第一列
        # 遍历字典列表
        for key,values in  dict.items():

            #判断是否第一列，做为x轴数据
            if i==0 :
                line_chart.x_labels =  values
            else :
                line_chart.add(key, values)

            i = i+1

        line_chart.render_to_file(svgFilename) 

        return None

    def _fDrawGraph(self, graphtype: int, dict: dict, svgFilename: str,title: str='table') ->None:
        """画指定类型的图表

        Args:
            graphtype (int): 要画什么类型的图表
            dict (dict): 表格数据
            svgFilename (str): 生成的svg全路径名
            title (str, optional): 表格标题. Defaults to 'table'.
        """
        if graphtype == const.GRAPH_LINE:
            return self._fDrawGraph_line(dict, svgFilename,title)
        elif graphtype == const.GRAPH_RANDAR:
            return self._fDrawGraph_Radar(dict, svgFilename,title)

        return None

    def _fAnalyseMDTablesDrawGraph(self, mdFilename: str, svgFilename: str, catchtableIndex: int=const.TABLE_ALL, graphtype: int=const.GRAPH_LINE) ->None:
        """分析md文件中所有的表格，并画出svg文件

        Args:
            mdFilename (str): 传入的md全路径文件名
            svgFilename (str): 要生成的svg全路径文件名
            catchtableIndex (int, optional): 指定md文件中的第几个表格. Defaults to const.TABLE_ALL.
            graphtype (int, optional): 指定图表类型. Defaults to const.GRAPH_LINE.
        """
        tables = self._fAnalyseTable(mdFilename)
        if tables == None:
            return

        tableindex = 0          #表格序号
        #表格循环
        for table in tables:

            '''
            table[0] : title
            table[1] : strtable
            '''

            #表格序号
            tableindex += 1

            #只输出指定序号的表格
            if catchtableIndex != tableindex and catchtableIndex != const.TABLE_ALL:
                continue

            d = self._fConvertTableToDict(table[1])
            if d == None:
                continue
            #print(d)

            #添加完成
            strsvgfilename = svgFilename
            if catchtableIndex == const.TABLE_ALL:
                #所有的表格都按序号输出
                lenfilename = len(strsvgfilename)
                strsvgfilename = strsvgfilename[0:lenfilename-4] + str(tableindex) + '.svg'

            self._fDrawGraph(graphtype, d, strsvgfilename,table[0])
    
    def _fconvertparmaeter(self, parameter: str) -> int:
        '''
        mdFilename
        svgFilename
        catchtableIndex
        graphtype
        '''
        d : dict
        ret = 0
        try:
            d = json.loads(parameter)

            self._mdFilename = d['mdFilename']
            self._svgFilename = d['svgFilename']
            self._catchtableIndex = int(d['catchtableIndex'])
            self._graphtype = int(d['graphtype'])
        except:
            ret = -1
        return ret

    def _fupdateparameter(self) ->str:
        d = dict()
        
        d.setdefault('mdFilename', self._mdFilename)
        d.setdefault('svgFilename', self._svgFilename)
        d.setdefault('catchtableIndex', self._catchtableIndex)
        d.setdefault('graphtype', self._graphtype)
        
        s : str
        s = json.dumps(d)
        
        self._parameter = s
        return s

    def _fcheckparmaeter(self) -> bool:
        if len(self._mdFilename) <= 0:
            return False
        if len(self._svgFilename) <= 0:
            return False
        return True

    def run(self) ->int :
        if self._fcheckparmaeter():
            self._fAnalyseMDTablesDrawGraph(self._mdFilename, self._svgFilename, self._catchtableIndex, self._graphtype)
        return 0
    
    def _fshowparameter(self, ui: taskmdgraph_setup.Ui_taskmdgraph_Dialog) -> None:
        ui.lineEdit_MDFile.setText(self._mdFilename)
        ui.lineEdit_SVGFile.setText(self._svgFilename)
        ui.lineEdit_tableindex.setText(str(self._catchtableIndex))
        
        if self._graphtype == const.GRAPH_LINE:
            ui.comboBox.setCurrentIndex(0)
        elif self._graphtype == const.GRAPH_RANDAR:
            ui.comboBox.setCurrentIndex(1)
        else:
            ui.comboBox.setCurrentIndex(0)
        
    def _fInitdialog(self, ui: taskmdgraph_setup.Ui_taskmdgraph_Dialog) -> None:
        ui.comboBox.addItems(['line','pandar'])
        ui.comboBox.setCurrentIndex(0)
        
    def _fgetdlgparameter(self, ui: taskmdgraph_setup.Ui_taskmdgraph_Dialog) ->None:
        self._mdFilename = ui.lineEdit_MDFile.text()
        self._svgFilename = ui.lineEdit_SVGFile.text()
        self._catchtableIndex = int(ui.lineEdit_tableindex.text())
        
        index = ui.comboBox.currentIndex()
        if index == 0:
            self._graphtype = const.GRAPH_LINE
        elif index == 1:
            self._graphtype = const.GRAPH_RANDAR
        else:
            self._graphtype = const.GRAPH_LINE
            
    def cfOnBtnmdfile(self, ui: taskmdgraph_setup.Ui_taskmdgraph_Dialog,dlg: QDialog) ->None:
        fname, ftype = QFileDialog.getOpenFileName(dlg, '选择打开的markdown文件',os.getcwd(),'Markdown files(*.md)')
        
        ui.lineEdit_MDFile.setText(fname)
    
    def cfOnBtnsvgfile(self, ui: taskmdgraph_setup.Ui_taskmdgraph_Dialog,dlg: QDialog) ->None:
        fname, ftype = QFileDialog.getSaveFileName(dlg, '选择保存的SVG文件',os.getcwd(),'SVG files(*.svg)')
        
        ui.lineEdit_SVGFile.setText(fname)

    def opensetup(self) -> int:
        
        ui = taskmdgraph_setup.Ui_taskmdgraph_Dialog()
        dlg = QDialog()
        ui.setupUi(dlg)

        ui.pushButton_mdfile.clicked.connect(partial(self.cfOnBtnmdfile,ui,dlg))
        ui.pushButton_svgfile.clicked.connect(partial(self.cfOnBtnsvgfile,ui,dlg))

        self._fInitdialog(ui)
        self._fshowparameter(ui)
        if dlg.exec():
            self._fgetdlgparameter(ui)
            self._fupdateparameter()

            return 0
        return -1

    def getname(self) -> str:
        return self._name

    def gettype(self) -> str:
        return self._tasktype

    def getparameter(self) -> str:
        return self._parameter

    def setparameter(self, parameter: str) -> int:
        self._parameter = parameter
        if len(parameter) > 0:
            return self._fconvertparmaeter(parameter)
        return 0

    def getpercent(self)-> int:
        return self._percent
