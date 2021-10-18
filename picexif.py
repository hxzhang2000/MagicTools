# coding = utf-8

import exifread as ef
import datetime
import const
import requests
import json

const.GAODE_KEY = '6c8c44d7fc90aa6b6a8b76e13cfd67b4'


class cPicExif:
    '一张图片exif信息'

    sPicname = ''                           #图片文件名

    dTime = ''                              #拍摄时间
    lat = 0.0                               #纬度
    lon = 0.0                               #经度
    altitude = 0.0                          #海拔
    sval = ''                               #位置文字

    def __init__(self, picname: str) -> None:
        self.sPicname = picname

    def __del__(self) -> None:
        pass

    def fGetPictureInfo(self) -> None:
        #print(self.sPicname)
        f = open(self.sPicname,'rb')
        img = ef.process_file(f,details=False,stop_tag='TAG')
        f.close()

        time = img.get('Image DateTime')
        if time != None:
            self.dTime = datetime.datetime.strptime(str(time),'%Y:%m:%d %H:%M:%S')
        else:
            self.dTime = None

        slat = img.get('GPS GPSLatitude')
        if slat != None:
            self.lat = self.convert_gps(slat)
        else :
            self.lat = None
        #print(self.lat)

        slon = img.get('GPS GPSLongitude')
        if slon != None:
            self.lon = self.convert_gps(slon)
        else:
            self.lon = None
        #print(self.lon)

        self.altitude = None
        saltitude = img.get('GPS GPSAltitude')
        if saltitude != None:
            saltitude = str(saltitude)
            if saltitude != '0' and saltitude.find('/') >= 0:
                self.altitude = float(saltitude.split('/')[0]) / float(saltitude.split('/')[1])
        #print(self.altitude)

    def convert_gps(self,coord_arr: str) -> float:
        arr = str(coord_arr).replace('[', '').replace(']', '').split(', ')
        d = float(arr[0])
        m = float(arr[1])

        n = arr[2].find('/')
        if n <= -1:
            return None

        s = float(arr[2].split('/')[0]) / float(arr[2].split('/')[1])

        return float(d) + (float(m) / 60) + (float(s) / 3600)

    def fregeo(self,lon: float,lat: float) -> str:
        if lon == None or lat == None:
            return None

        template = 'https://restapi.amap.com/v3/geocode/regeo?output=JSON&location={lon},{lat}&key={key}'

        url = template.format(lon=lon, lat=lat, key=const.GAODE_KEY)
        resp = requests.get(url)

        data : dict
        addressComponent : dict
        
        data = json.loads(resp.text)
        status = int(data['status'])
        if status != 1:
            return None
        addressComponent = data.get('regeocode').get('addressComponent')
        province = addressComponent.get('province')
        if len(province) <= 0:
            province = ''
        city = addressComponent.get('city')
        if len(city) <= 0:
            city = ''
        district = addressComponent.get('district')
        if len(district) <= 0:
            district = ''

        self.sval = province + city + district

        return self.sval

