#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import urllib2
from bs4 import BeautifulSoup


def GetHuiLV(fcur,tcurs):
    result = ''
    for tcur in tcurs:
        url = 'http://qq.ip138.com/hl.asp?from=%s&to=%s&q=100' % (fcur,tcur)
        print url
        content = urllib2.urlopen(url).read()
        '''td = TD()
        td.feed(content)
        result += "%s %s 兑换 %s %s %s %s\n" % (td.name[0],td.name[3],td.name[2],td.name[5],td.name[1],td.name[4])
        '''
        html=urllib2.urlopen(url)
        print type(html)
        obj=BeautifulSoup(html.read(),'html.parser')
        trs=obj.find_all('tr')
        if len(trs)>2:
            tds=trs[2].find_all('td')
            for td in tds:
                result+=td.text+'\t'
        #soup = BeautifulSoup(content)
        #print soup.prettify()
        #print content
        
        #result += content
    print result
    return result

if __name__ == '__main__':
    GetHuiLV( 'CNY',['USD','MOP','JPY'])