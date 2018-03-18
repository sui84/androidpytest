#encoding=utf-8
import time
import datetime
'''
time.time()
time.localtime()
time.gmtime()
time.mktime(time.localtime())
'''

def GetCurrentTimeStr(fmt='%Y/%m/%d %H:%M:%S'):
    return time.strftime(fmt)

def AddDate(basedt =datetime.datetime.now(), days=0,hours=0,mins=0):
    d = basedt+datetime.timedelta(days=days,hours=hours,minutes=mins)
    return d

def GetDateDiff(date1, date2):
    return abs(date2-date1).days

def GetDayDiff(dnum1,dnum2):
    # date1 =time.localtime(time.time())
    # date2 =time.localtime(fattrs.st_mtime)
    # (arrow.get(1521372536)-arrow.get(1519486889)).days 相隔天数
    # (datetime.date(a.tm_year,a.tm_mon,a.tm_mday)-datetime.date(b.tm_year,b.tm_mon,b.tm_mday)).days
    date1,date2 =time.localtime(dnum1),time.localtime(dnum2)
    return (datetime.date(date2.tm_year,date2.tm_mon,date2.tm_mday)-datetime.date(date1.tm_year,date1.tm_mon,date1.tm_mday)).days

def GetYearMonths(offset):
    #往前或往后多少个月
    yearmonths = []
    now = self.GetNow()
    y = curyear = now.year
    curmonth = now.month
    for i in range(0,abs(offset)):
        if offset > 0 :
            m = (curmonth+i-1)%12+1
        else:
            m =(curmonth-i-1)%12+1
        if i>0 and m==1 and offset > 0 :
            y +=1
        if i>0 and m==12  and offset < 0 :
            y -=1
        yearmonths.append({"year":y,"month":m})
    return yearmonths

def GetNow():
    # year : datetime.datetime.now().year
    return datetime.datetime.now()

def elapsedtimedeco(arg=True):
    if arg:
        def _deco(func):
            def wrapper(*args,**kwargs):
                startTime = time.time()
                func(*args,**kwargs)
                endTime = time.time()
                msecs = (endTime - startTime) * 1000
                print "->elapsed time: %f ms" % msecs
            return wrapper
    else:
        def _deco(func):
            return func
    return _deco

if __name__ == '__main__':
    # 装饰器使用
    @elapsedtimedeco(True)
    def addFunc(a,b,c):
        print 'start'
        time.sleep(0.9)
        print a+b+c
        print 'end'

    addFunc(5,6,8)
