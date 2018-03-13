import androidhelper
droid = androidhelper.Android()
code = droid.scanBarcode()
isbn = code[1]['extras']['SCAN_RESULT']
print isbn
url = "http://book.douban.com/subject_search?search_text=%s&cat=1001"%isbn
droid.startActivity("android.intent.action.VIEW",url)
