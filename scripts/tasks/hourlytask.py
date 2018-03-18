#coding:utf-8
import os
import sys
from threading import Timer
reload(sys)
sys.setdefaultencoding('utf8')
parentpath =os.path.join(os.path.dirname(os.path.realpath(__file__)),'..')
sys.path.append(parentpath)
from utils import loghelper
import apihelper


timediff=60*60*12  # 12 hours
count=0
logger = loghelper.create_logger(loghelper.LOGPATH)
@loghelper.exception(logger)
@loghelper.stdouttofile(loghelper.LOGPATH)
def hourly_schedule(msg,starttime):
    global count
    count+=1
    print 'call times:', count
    ah =apihelper.ApiHelper()
    ah.GetHuiLV( 'CNY',['USD','MOP','JPY'])
    ah.weather_jwdus(['kyoto','大阪','珠海','奈良'])
    ah.weather_citys(['kyoto',u'大阪',u'珠海',u'奈良'])
    #ah.location(( 21.9745252,113.931350085))
    Timer(timediff,hourly_schedule,()).start()


if __name__ == '__main__':
    Timer(timediff,hourly_schedule,()).start()

