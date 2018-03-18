
def url_jsonobj(url):
    import urllib2
    import json
    content = urllib2.urlopen(url).read()
    jsonobj =json.loads(content)
    return jsonobj

