import htmllib, formatter, urllib, urlparse
from urllib2 import Request, urlopen, URLError, HTTPError
import os


seen = {}
p = htmllib.HTMLParser(formatter.NullFormatter(  ))
originalurl = 'http://wikimediafoundation.org/wiki/Lahjoitukset'

seen[originalurl] = True
try:
    
##    f, headers = urllib.urlretrieve(originalurl)
##    print f
##    statinfo = os.stat(f)
##    f = urllib.pathname2url(f)
##    
##    print statinfo.st_size
    f = urllib.urlopen(originalurl)
##    print headers
##    print f.code
##    originalurl = f.geturl()
##    print 'Redirected: ', originalurl

    if originalurl not in seen:
        seen[originalurl] = True

    headers = f.info()
    print headers
    ##print 'Content-Type: ', headers['Content-Type']
    ##print 'Length: ', headers['Content-Length']


    BUFSIZE = 8192
    while True:
        data = f.read(BUFSIZE)
        if not data: break
        p.feed(data)

    #print 'Length: ', len(data)

    p.close(  )

except IOError, e:
    print e


for url in p.anchorlist:

    pieces = urlparse.urlparse(url)
    print pieces.geturl()
#    if pieces[0] == 'http':
#        print urlparse.urlunparse(pieces)
    
    temp, fragment = urlparse.urldefrag(url)
    temp = urlparse.urljoin(originalurl,'///') + 'robot.txt'
    print temp
    if temp in seen: continue
    seen[temp] = True
    parsedurl = urlparse.urlparse(temp)
    if parsedurl[0] == 'mailto':
        continue
    #if parsedurl[0] == 'javascript':
    print urlparse.urlunparse(parsedurl)
