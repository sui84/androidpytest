#encoding=utf-8
import logging
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import time
import traceback
import os

LOGPATH = '/storage/emulated/0/qpython/scripts/log.txt'
if not os.path.isfile(LOGPATH):
    LOGPATH = 'log.txt'
    
def exception(logger):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                msg = "funcname=%s,args=%s,kwargs=%s" % (func.__name__ ,args , kwargs)
                logger.info(msg)
                return func(*args, **kwargs)
            except:
                # log the exception
                err = "exception : funcname=%s,args=%s,kwargs=%s" % (func.__name__ ,args , kwargs)
                logger.exception(err)
 
            # re-raise the exception
            raise
        return wrapper
    return decorator
    
    
def create_logger(logpath):
    logger = logging.getLogger("testlogger")
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler(logpath)
    fmt = '[%(asctime)s - %(name)s - %(levelname)s %(process)d %(processName)s %(thread)d %(threadName)s] %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
 
    # add handler to logger object
    logger.addHandler(fh)
    return logger

logger = create_logger(LOGPATH)
@exception(logger)
def zero_divide(i,j):
    i/j

def stdouttofile(logpath):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                with open (logpath,'a') as f:
                    __console__=sys.stdout
                    sys.stdout=f
                    print '\n',time.asctime(time.localtime(time.time()))
                    result = func(*args, **kwargs)
                    sys.stdout=__console__
                    return result
            except:
                pass
        return wrapper
    return decorator

@stdouttofile(LOGPATH)
def testlog(a,b):
    print a,b
    return a+b

class logex(object):
    def __init__(self,logger):
        self.logger = logger

    def __call__(self,func):
        def _call(*args,**kwargs):
            try:
                msg = "funcname=%s,args=%s,kwargs=%s" % (func.__name__ ,args , kwargs)
                self.logger.info(msg)
            except Exception,e:
                err =  time.ctime()+ 'Error:'+e.message+'\n'+traceback.format_exc()
                self.logger.exception(err)
            return func(*args,**kwargs)
        return _call

if __name__ == '__main__':
    #zero_divide(1,0)
    zero_divide(1,1)
