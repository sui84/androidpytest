from androidhelper import Android
import sys
reload(sys)
sys.setdefaultencoding('utf8')


droid = Android()
#setClipboard
#droid.setClipboard("Hello World")
#getClipboard
clipboard = droid.getClipboard().result

#droid.notify('Hello','QPython')
print clipboard
