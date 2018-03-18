#coding:utf-8
import os
import sys
from androidhelper import Android
reload(sys)
sys.setdefaultencoding('utf8')
parentpath =os.path.join(os.path.dirname(os.path.realpath(__file__)),'..')
sys.path.append(parentpath)
from utils import loghelper,common
from db import savedb
from threading import Timer
import time
import traceback
import pprint


timediff=60*5 # half an hour
addressurl='http://gc.ditu.aliyun.com/regeocoding?l=%s,%s&type=111'
logger = loghelper.create_logger(loghelper.LOGPATH)
db = savedb.get_db()


@loghelper.exception(logger)
#@loghelper.stdouttofile(loghelper.LOGPATH)
def minly_schedule():
    clipboard()
    location()
    Timer(timediff,minly_schedule,()).start()

@loghelper.stdouttofile(loghelper.LOGPATH)
def clipboard():
    try:
        print 'current clipboard() time:',time.asctime(time.localtime(time.time()))
        droid = Android()
        #setClipboard
        #droid.setClipboard("Hello World")
        #getClipboard
        cbstr = droid.getClipboard().result
        print cbstr
        if db <> None and cbstr<> None and len(cbstr)>0:
            sql="insert into info(createdby,comment) values('%s','%s')" % ('minlytask.clipboard',cbstr)
            db.ExecNonQuery(sql)
    except Exception,e:
        print e.message,traceback.format_exc()

#@loghelper.stdouttofile(loghelper.LOGPATH)
def location():
    try:
        print 'current location() time:',time.asctime(time.localtime(time.time()))
        droid = Android()
        droid.startLocating()
        location = droid.getLastKnownLocation().result
        pprint.pprint(location)
        content = 'haiba:%s\tjdu:%s\twdu:%s\tspeed:%s\tprovider:%s\taccuracy:%s'
        gps = location.get('gps')
        network = location.get('gps')
        passive = location.get('gps')
        if gps<> None:
            altitude,longitude,latitude,speed,provider,accuracy=gps.get('altitude'),gps.get('longitude'),gps.get('latitude'),gps.get('speed'),gps.get('provider'),gps.get('accuracy')
            pprint.pprint(content % (altitude,longitude,latitude,speed,provider,accuracy))
        else:
            jdu,wdu,speed=0,0,0
        if network<> None:
            print content % (network.get('altitude'),network.get('longitude'),network.get('latitude'),network.get('speed'),network.get('provider'),network.get('accuracy'))
        if passive<> None:
            print content % (passive.get('altitude'),passive.get('longitude'),passive.get('latitude'),passive.get('speed'),passive.get('provider'),passive.get('accuracy'))
        location = location.get('network', location.get('gps'))
        wdu,jdu = location.get('latitude'),location.get('longitude')
        url=addressurl % (wdu,jdu)
        print url
        obj = common.url_jsonobj(url)
        print obj.get('queryLocation')
        addresslist = obj.get('addrList')
        for address in addresslist:
            if address.get('name')<>'':
                add =  'admCode:%s\tadmName:%s\t%s\ndistance:%s\tnearestPoint:%s\ttype:%s\tstatus:%s' % (address.get('admCode'),address.get('admName'),address.get('distance'),address.get('name'),address.get('nearestPoint'),address.get('type'),address.get('status'))
                print add
                if db <> None :
                    sql="insert into info(createdby,comment,altitude,longitude,latitude,speed,provider,accuracy) values('%s','%s',%f,%f,%f,%f,'%s',%d)" % ('minlytask.location',add,altitude,longitude,latitude,speed,provider,accuracy)
                    db.ExecNonQuery(sql)

    except Exception,e:
        print e.message,traceback.format_exc()


def sms():
    droid = Android()
    s=droid.smsSend("15919147090","测试")

'''
Droid.startSensingTimed(1, 250)
sensor = Droid.sensorsReadOrientation().result
Droid.stopSensing()
'''

#droid.notify('Hello','QPython')

if __name__ == '__main__':
    #Timer(timediff,minly_schedule,()).start()
    sms()
    exit(0)
    clipboard()
    location()


