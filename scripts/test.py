#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import urllib2
from bs4 import BeautifulSoup
from PIL import Image

def resizeimg():
    ifile = '/storage/emulated/0/Pictures/表情/test.jpg'
    ofile = '/storage/emulated/0/Pictures/表情/out/test.jpg'
    im = Image.open(ifile)
    #im.resize((200,100),Image.ANTIALIAS).save(ofile, "PNG", quality=100)
    im.resize((200,100))
    im.save(ofile)
    print u'等比压缩完成',ifile


if __name__ == '__main__':
    resizeimg()
