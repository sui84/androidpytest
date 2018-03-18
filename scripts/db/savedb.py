#coding:utf-8
import os
import sys
from threading import Timer
reload(sys)
sys.setdefaultencoding('utf8')
parentpath =os.path.join(os.path.dirname(os.path.realpath(__file__)),'..')
sys.path.append(parentpath)
from utils import sockethelper

def get_db():
    import sqlhelper
    s = sockethelper.SocketHelper()
    dbs = [{'server':'192.168.1.1','port':3306}]
    server,port = dbs[0].get('server'),dbs[0].get('port')
    netok = s.telnet(server,port)
    if not netok:
        server,port = dbs[1].get('server'),dbs[1].get('port')
        netok = s.telnet(server,port)
    if netok:
        print 'db connection :',server,port
        mydb = sqlhelper.SqlHelper(host=server,port=port,user="root",pwd="test",db="log",dbtype='mysql')
        return mydb
    else:
        return None




