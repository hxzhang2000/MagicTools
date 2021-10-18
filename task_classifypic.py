# coding = utf-8

from taskinterface import taskinterface
from sys import setswitchinterval
import const
import json
import os
import shutil
from PyQt6.QtWidgets import QFileDialog
from tqdm import tqdm
from picexif import cPicExif

const.CLASSIFYPIC_NAME = 'classify picture'

class task_classifypic(taskinterface):
    
    def __init__(self) -> None:
        self._name = const.CLASSIFYPIC_NAME
        self._tasktype = 'tools'
        self._parameter = ''

        self._picpath = r'C:\hxzhang\照片\wfx照片'
        
        super().__init__()
    
    
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

    def _fGetPathFromFilename(self, sFilename: str) -> list:
        index = sFilename.rfind('\\')
        if index == -1:
            return None
        return [sFilename[0:index],sFilename[index+1:]]

    def _fOpDir(self, sPathname: str) -> None:
        if os.path.exists(sPathname):
            return
        os.mkdir(sPathname)
    
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

    def run(self) -> int:
        if not self._fcheckparmaeter():
            return -1
        
        files = self._flist_allfile(self._picpath)
        total = len(files)
        pbar = tqdm(total=total , desc=const.CLASSIFYPIC_NAME)
        
        i = 0

        for filename in files:
            
            pbar.update(1)
            i = i + 1
            self._percent = i / (total/ 100)

            cp = cPicExif(filename)
            cp.fGetPictureInfo()

            sval = cp.fregeo(cp.lon,cp.lat)
            if sval == None:
                continue

            fl = self._fGetPathFromFilename(filename)
            if fl == None:
                continue
            spathname = fl[0]
            fn = fl[1]

            spathname += '\\{date}-{val}'
            spathname = spathname.format(date= cp.dTime.strftime('%Y%m%d'),val=sval)

            self._fOpDir(spathname)
            newname = os.path.join(spathname, fn)
            shutil.move(filename, newname)
            
        pbar.close()
        
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



