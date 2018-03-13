#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import urllib2
from bs4 import BeautifulSoup
import loghelper
#import requests
import geohelper
import pprint
import HTMLParser
import json
import traceback

logger = loghelper.create_logger(loghelper.LOGPATH)

class ApiHelper(object):
    def __init__(self):
        #self.sh = strhelper.StrHelper()
        self.hp =HTMLParser.HTMLParser()
        self.weatherurl_city='http://www.sojson.com/open/api/weather/json.shtml?city=%s'
        self.weatherurl_jwu='http://www.caiyunapp.com/fcgi-bin/v1/api.py?lonlat=%.2f,%.2f&format=json&product=minutes_prec&token=96Ly7wgKGq6FhllM&random=0.8600497214532319)'
        self.gh = geohelper.GeoHelper()
        self.ipurls = ['http://ip.chinaz.com/getip.aspx']
        self.jwus = {u'珠海': ( 21.9745252,113.931350085),u'大阪': ( 34.704365,135.501887),'kyoto': (35.0231321,135.7634074),u'奈良': ( 34.684545,135.804836)}

    def GetResult(self,trs,idx):
        result = ''
        tds=trs[idx].find_all('td')
        result+='\n'
        for td in tds:
            result+=td.text+'\t'
        return result


    @loghelper.exception(logger)
    @loghelper.stdouttofile(loghelper.LOGPATH)
    def GetHuiLV(self,fcur,tcurs):
        result = ''
        idx = 1
        for tcur in tcurs:
            url = 'http://qq.ip138.com/hl.asp?from=%s&to=%s&q=100' % (fcur,tcur)
            print url
            content = urllib2.urlopen(url).read()
            html=urllib2.urlopen(url)
            #soup = BeautifulSoup(content)  not work
            obj=BeautifulSoup(html.read(),'html.parser')
            trs=obj.find_all('tr')
            result+=self.GetResult(trs,1)
            result+=self.GetResult(trs,2)
        print result
        return result

    @loghelper.exception(logger)
    @loghelper.stdouttofile(loghelper.LOGPATH)
    def weather_jwdus(self,citys):
        for city in citys:
            try:
                self.weather_jwdu(city)
            except Exception,e:
                 print traceback.format_exc()

    def weather_jwdu(self,city):
        jwu = self.jwus.get(city)
        if jwu == None:
            try:
                (wdu,jdu) = self.gh.GetWJdu(city)
            except Exception,e:
                 print u'获取 %s 经纬度失败 ' % city
        else:
            (wdu,jdu) = jwu
        result = u"纬度:%f\n经度:%f\n" %(wdu,jdu)
        url = self.weatherurl_jwu % (jdu,wdu)
        #req = requests.get(url)
        #obj =json.loads(req.text)
        html=urllib2.urlopen(url)
        obj =json.loads(html.read())
        result +=  '%s Location:%s 温度:%s %s' % (city,obj['location'],obj['temp'],obj['summary'])
        print result
        return result
        '''
        >>> pprint.pprint(obj)
{u'api_status': u'deprecated',
u'api_version': u'v1.2',
u'dataseries': [0.0,
            ...
             0.0],
u'location': [21.97, 113.93],
u'nearest_rain': {u'direction': 334.0813598633,
               u'distance': 134.2449655593,
               u'intensity': 0.1875},
u'previous': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
u'radar_img': [[u'/res/storm_radar/radar_AZ9200_nmc_fast/20180313/SEVP_AOC_RDCP_SLDAS_EBREF_AZ9200_L88_PI_20180313115400000.clean.png',
             1520942041.0,
             [20.8635367336,
              111.0382357073,
              25.1395192664,
              115.6835462927]],
            [u'/res/storm_radar/radar_AZ9200_nmc_fast/20180313/SEVP_AOC_RDCP_SLDAS_EBREF_AZ9200_L88_PI_20180313120000000.clean.png',
             1520942401.0,
             [20.8635367336,
              111.0382357073,
              25.1395192664,
              115.6835462927]],
            [u'/res/storm_radar/radar_AZ9200_nmc_fast/20180313/SEVP_AOC_RDCP_SLDAS_EBREF_AZ9200_L88_PI_20180313120600000.clean.png',
             1520942761.0,
             [20.8635367336,
              111.0382357073,
              25.1395192664,
              115.6835462927]],
            [u'/res/storm_radar/radar_AZ9200_nmc_fast/20180313/SEVP_AOC_RDCP_SLDAS_EBREF_AZ9200_L88_PI_20180313121200000.clean.png',
             1520943122.0,
             [20.8635367336,
              111.0382357073,
              25.1395192664,
              115.6835462927]],
            [u'/res/storm_radar/radar_AZ9200_nmc_fast/20180313/SEVP_AOC_RDCP_SLDAS_EBREF_AZ9200_L88_PI_20180313121800000.clean.png',
             1520943481.0,
             [20.8635367336,
              111.0382357073,
              25.1395192664,
              115.6835462927]],
            [u'/res/storm_radar/radar_AZ9200_nmc_fast/20180313/SEVP_AOC_RDCP_SLDAS_EBREF_AZ9200_L88_PI_20180313122400000.clean.png',
             1520943841.0,
             [20.8635367336,
              111.0382357073,
              25.1395192664,
              115.6835462927]],
            [u'/res/storm_radar/radar_AZ9200_nmc_fast/20180313/SEVP_AOC_RDCP_SLDAS_EBREF_AZ9200_L88_PI_20180313123000000.clean.png',
             1520944201.0,
             [20.8635367336,
              111.0382357073,
              25.1395192664,
              115.6835462927]],
            [u'/res/storm_radar/radar_AZ9200_nmc_fast/20180313/SEVP_AOC_RDCP_SLDAS_EBREF_AZ9200_L88_PI_20180313123600000.clean.png',
             1520944561.0,
             [20.8635367336,
              111.0382357073,
              25.1395192664,
              115.6835462927]],
            [u'/res/storm_radar/radar_AZ9200_nmc_fast/20180313/SEVP_AOC_RDCP_SLDAS_EBREF_AZ9200_L88_PI_20180313124200000.clean.png',
             1520944921.0,
             [20.8635367336,
              111.0382357073,
              25.1395192664,
              115.6835462927]],
            [u'/res/storm_radar/radar_AZ9200_nmc_fast/20180313/SEVP_AOC_RDCP_SLDAS_EBREF_AZ9200_L88_PI_20180313124800000.clean.png',
             1520945282.0,
             [20.8635367336,
              111.0382357073,
              25.1395192664,
              115.6835462927]],
            [u'/res/storm_radar/radar_AZ9200_nmc_fast/20180313/SEVP_AOC_RDCP_SLDAS_EBREF_AZ9200_L88_PI_20180313125400000.clean.png',
             1520945641.0,
             [20.8635367336,
              111.0382357073,
              25.1395192664,
              115.6835462927]],
            [u'/res/storm_radar/radar_AZ9200_nmc_fast/20180313/SEVP_AOC_RDCP_SLDAS_EBREF_AZ9200_L88_PI_20180313130000000.clean.png',
             1520946001.0,
             [20.8635367336,
              111.0382357073,
              25.1395192664,
              115.6835462927]],
            [u'/res/storm_radar/radar_AZ9200_nmc_fast/20180313/SEVP_AOC_RDCP_SLDAS_EBREF_AZ9200_L88_PI_20180313130600000.clean.png',
             1520946361.0,
             [20.8635367336,
              111.0382357073,
              25.1395192664,
              115.6835462927]],
            [u'/res/storm_radar/radar_AZ9200_nmc_fast/20180313/SEVP_AOC_RDCP_SLDAS_EBREF_AZ9200_L88_PI_20180313131200000.clean.png',
             1520946722.0,
             [20.8635367336,
              111.0382357073,
              25.1395192664,
              115.6835462927]],
            [u'/res/storm_radar/radar_AZ9200_nmc_fast/20180313/SEVP_AOC_RDCP_SLDAS_EBREF_AZ9200_L88_PI_20180313131800000.clean.png',
             1520947081.0,
             [20.8635367336,
              111.0382357073,
              25.1395192664,
              115.6835462927]],
            [u'/res/storm_radar/radar_AZ9200_nmc_fast/20180313/SEVP_AOC_RDCP_SLDAS_EBREF_AZ9200_L88_PI_20180313132400000.clean.png',
             1520947441.0,
             [20.8635367336,
              111.0382357073,
              25.1395192664,
              115.6835462927]],
            [u'/res/storm_radar/radar_AZ9200_nmc_fast/20180313/SEVP_AOC_RDCP_SLDAS_EBREF_AZ9200_L88_PI_20180313133000000.clean.png',
             1520947801.0,
             [20.8635367336,
              111.0382357073,
              25.1395192664,
              115.6835462927]],
            [u'/res/storm_radar/radar_AZ9200_nmc_fast/20180313/SEVP_AOC_RDCP_SLDAS_EBREF_AZ9200_L88_PI_20180313133600000.clean.png',
             1520948162.0,
             [20.8635367336,
              111.0382357073,
              25.1395192664,
              115.6835462927]],
            [u'/res/storm_radar/radar_AZ9200_nmc_fast/20180313/SEVP_AOC_RDCP_SLDAS_EBREF_AZ9200_L88_PI_20180313134200000.clean.png',
             1520948521.0,
             [20.8635367336,
              111.0382357073,
              25.1395192664,
              115.6835462927]],
            [u'/res/storm_radar/radar_AZ9200_nmc_fast/20180313/SEVP_AOC_RDCP_SLDAS_EBREF_AZ9200_L88_PI_20180313134800000.clean.png',
             1520948881.0,
             [20.8635367336,
              111.0382357073,
              25.1395192664,
              115.6835462927]]],
u'server_time': 1520949274,
u'skycon': u'PARTLY_CLOUDY_NIGHT',
u'source': u'radar',
u'station': u'AZ9200',
u'status': u'ok',
u'summary': u'\u672a\u6765\u4e24\u5c0f\u65f6\u4e0d\u4f1a\u4e0b\u96e8\uff0c\u653e\u5fc3\u51fa\u95e8\u5427',

u'temp': 20.0}'''

    @loghelper.exception(logger)
    @loghelper.stdouttofile(loghelper.LOGPATH)
    def weather_citys(self,citys):
        for city in citys:
            try:
                self.weather_city(city)
            except Exception,e:
                 print traceback.format_exc()

    def weather_city(self,city):
        try:
            (wdu,jdu) = self.gh.GetWJdu(city)
            result = u"纬度:%f\n经度:%f\n" %(wdu,jdu)
            print result
        except Exception,e:
            print u'获取 %s 经纬度失败 ' % city
        url = self.weatherurl_city % city
        #req = requests.get(url)
        #datadict=self.hp.unescape(self.sh.Jsonstr2Obj(req.text))
        #datadict = json.loads(req.text)
        html=urllib2.urlopen(url)
        datadict =json.loads(html.read())
        '''
        print datadict
        pprint.pprint(datadict)
        {u'city': u'\u73e0\u6d77',
 u'count': 39,
 u'data': {u'forecast': [{u'aqi': 38.0,
                          u'date': u'15\u65e5\u661f\u671f\u65e5',
                          u'fl': u'4-5\u7ea7',
                          u'fx': u'\u4e1c\u5317\u98ce',
                          u'high': u'\u9ad8\u6e29 26.0\u2103',
                          u'low': u'\u4f4e\u6e29 23.0\u2103',
                          u'notice': u'\u5c3d\u91cf\u51cf\u5c11\u6237\u5916\u6d3b\u52a8\uff0c\u9632\u6b62\u610f\u5916\u53d1\u751f',
                          u'sunrise': u'06:21',
                          u'sunset': u'18:01',
                          u'type': u'\u66b4\u96e8'},
                         {u'aqi': 27.0,
                          u'date': u'16\u65e5\u661f\u671f\u4e00',
                          u'fl': u'<3\u7ea7',
                          u'fx': u'\u65e0\u6301\u7eed\u98ce\u5411',
                          u'high': u'\u9ad8\u6e29 27.0\u2103',
                          u'low': u'\u4f4e\u6e29 23.0\u2103',
                          u'notice': u'\u613f\u96e8\u540e\u6e05\u65b0\u7684\u7a7a\u6c14\u7ed9\u60a8\u5e26\u6765\u597d\u5fc3\u60c5\uff01',
                          u'sunrise': u'06:21',
                          u'sunset': u'18:00',
                          u'type': u'\u9635\u96e8'},
                         {u'aqi': 31.0,
                          u'date': u'17\u65e5\u661f\u671f\u4e8c',
                          u'fl': u'<3\u7ea7',
                          u'fx': u'\u65e0\u6301\u7eed\u98ce\u5411',
                          u'high': u'\u9ad8\u6e29 29.0\u2103',
                          u'low': u'\u4f4e\u6e29 24.0\u2103',
                          u'notice': u'\u4eca\u65e5\u591a\u4e91\uff0c\u9a91\u4e0a\u5355\u8f66\u53bb\u770b\u770b\u4e16\u754c\u5427',
                          u'sunrise': u'06:22',
                          u'sunset': u'18:00',
                          u'type': u'\u591a\u4e91'},
                         {u'aqi': 59.0,
                          u'date': u'18\u65e5\u661f\u671f\u4e09',
                          u'fl': u'<3\u7ea7',
                          u'fx': u'\u65e0\u6301\u7eed\u98ce\u5411',
                          u'high': u'\u9ad8\u6e29 29.0\u2103',
                          u'low': u'\u4f4e\u6e29 24.0\u2103',
                          u'notice': u'\u60a0\u60a0\u7684\u4e91\u91cc\u6709\u6de1\u6de1\u7684\u8bd7',
                          u'sunrise': u'06:22',
                          u'sunset': u'17:59',
                          u'type': u'\u591a\u4e91'},
                         {u'aqi': 74.0,
                          u'date': u'19\u65e5\u661f\u671f\u56db',
                          u'fl': u'<3\u7ea7',
                          u'fx': u'\u65e0\u6301\u7eed\u98ce\u5411',
                          u'high': u'\u9ad8\u6e29 29.0\u2103',
                          u'low': u'\u4f4e\u6e29 24.0\u2103',
                          u'notice': u'\u7ef5\u7ef5\u7684\u4e91\u6735\uff0c\u5f62\u72b6\u5343\u53d8\u4e07\u5316',
                          u'sunrise': u'06:23',
                          u'sunset': u'17:58',
                          u'type': u'\u591a\u4e91'}],
           u'ganmao': u'\u5404\u7c7b\u4eba\u7fa4\u53ef\u81ea\u7531\u6d3b\u52a8',
           u'pm10': 33.0,
           u'pm25': 21.0,
           u'quality': u'\u4f18',
           u'shidu': u'71%',
           u'wendu': u'22',
           u'yesterday': {u'aqi': 45.0,
                          u'date': u'14\u65e5\u661f\u671f\u516d',
                          u'fl': u'3-4\u7ea7',
                          u'fx': u'\u4e1c\u5317\u98ce',
                          u'high': u'\u9ad8\u6e29 28.0\u2103',
                          u'low': u'\u4f4e\u6e29 23.0\u2103',
                          u'notice': u'\u4eca\u65e5\u591a\u4e91\uff0c\u9a91\u4e0a\u5355\u8f66\u53bb\u770b\u770b\u4e16\u754c\u5427',
                          u'sunrise': u'06:21',
                          u'sunset': u'18:02',
                          u'type': u'\u591a\u4e91'}},
 u'date': u'20171015',
 u'message': u'Success !',
 u'status': 200}
       '''
        if datadict.get("status") == 200:
            data = datadict["data"]
            yesterday = data['yesterday']
            forecast = data['forecast']
            count = datadict["count"]
            citystr = datadict["city"]
            datestr = datadict["date"]
            shidu = data["shidu"]
            wendu = data["wendu"]
            pm25 = data.get("pm25")
            quality = data["quality"]
            sunrise = yesterday['sunrise']
            sunset = yesterday['sunset']
            result= u"%s\t%s\n温度:%s\t湿度:%s\tPM25:%d %s\n%s\t%s" % (citystr,datestr,wendu,shidu,pm25,quality,sunrise,sunset)
            result+=u"%s %s %s %s\n %s~%s\n"  % (yesterday['date'],yesterday['type'],yesterday['fx'],yesterday['fl']
                                                  ,yesterday['low'],yesterday['high'])
            for i in range(0,len(forecast)-1):
                result+=u"%s %s %s %s\n %s~%s\n"  % (forecast[i]['date'],forecast[i]['type'],forecast[i]['fx'],forecast[i]['fl']
                                                   ,forecast[i]['low'],forecast[i]['high'])
        else:
            result = u'获取%s天气失败:%s' % (city,datadict["message"])
        print result
        return result

    def location(self,wjdu):
        data = self.gh.GetLocation(wjdu)
        result = "纬度:%s\n经度:%s\n%s" % (data.get('lat'),data.get('lon'),data.get('display_name'))
        state_district = data.get('address').get('state_district')
        city = state_district.split('/')[0].strip()
        pprint.pprint(city)
        cweather = self.weather(city)
        result += "\n" + cweather
        return result

if __name__ == '__main__':
    ah =ApiHelper()
    #ah.GetHuiLV( 'CNY',['USD','MOP','JPY'])
    ah.weather_jwdus(['kyoto',u'大阪',u'珠海',u'奈良'])
    ah.weather_citys(['kyoto',u'大阪',u'珠海',u'奈良'])


