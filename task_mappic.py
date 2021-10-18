# coding = utf-8

from taskinterface import taskinterface
import json
import tqdm
from picexif import cPicExif
import os
from PyQt6.QtWidgets import QFileDialog
import const
import pandas as pd

const.MAPPIC_NAME = 'map picture'

class task_mappic(taskinterface):
    def __init__(self) -> None:
        self._name = const.MAPPIC_NAME
        self._tasktype = 'tools'
        self._parameter = ''

        self._picpath = r'C:\hxzhang\照片\wfx照片'
        
        super().__init__()
    
    def _fconvertparmaeter(self, parameter: str) -> None:
        '''
        picpath
        '''
        d : dict
        ret = 0
        try:
            d = json.loads(parameter)

            self._picpath = d['picpath']
        except:
            ret = -1
        return ret

    def _fupdateparameter(self) -> str:
        d = dict()
        
        d.setdefault('picpath', self._picpath)
        
        s : str
        s = json.dumps(d)
        
        self._parameter = s
        return s

    def _fcheckparmaeter(self) -> bool:
        if len(self._picpath) <= 0:
            return False
        return True
    
    def _flist_allfile(self, path: str,all_files: list = []) -> list:
        if os.path.exists(path):
            files=os.listdir(path)
        else:
            print('this path not exist')
        for file in files:
            if os.path.isdir(os.path.join(path,file)):
                self._flist_allfile(os.path.join(path,file),all_files)
            else:
                all_files.append(os.path.join(path,file))
        return all_files

    def _fadditem(self, df :pd.DataFrame, name :str, pe : cPicExif) -> pd.DataFrame:
        dfname = df.append(
            {"name": '', "date": pe.dTime, "pos": str(pe.lon)+ ',' + str(pe.lat),"altitude":pe.altitude}, ignore_index=True)
        return dfname

    def run(self) -> int:
        if not self._fcheckparmaeter():
            return -1
        
        files = self._flist_allfile(self._picpath)
        total = len(files)
        #pbar = tqdm(total=total , desc='map picture')
        
        i = 0
        
        dfname = pd.DataFrame()
        dfname['name'] = None
        dfname['date'] = None
        dfname['pos'] = None
        dfname['altitude'] = None

        for filename in files:
            
            #pbar.update(1)
            i = i + 1
            self._percent = i / (total/ 100)

            cp = cPicExif(filename)
            cp.fGetPictureInfo()
            
            if cp.lat != None and cp.lon != None:
                dfname = self._fadditem(dfname, filename, cp)

        #print(dfname)
        dfname.to_csv("mappic.csv", index= True, index_label='id')
        #pbar.close()
        
        return 0

    
    def opensetup(self) -> int:
        s = QFileDialog.getExistingDirectory(None, '请选择图片目录', self._picpath)
        
        if len(s) > 0:
            self._picpath = s
            
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
    
    def getpercent(self) -> int:
        return self._percent
