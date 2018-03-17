import urllib2
import json

def  url_jsonobj(url):
    content = urllib2.urlopen(url).read()
    jsonobj =json.loads(content)
    return jsonobj
