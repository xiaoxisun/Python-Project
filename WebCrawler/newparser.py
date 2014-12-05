#from HTMLParser import HTMLParser
import htmllib
import urllib
import formatter
import urlparse
from SimpleCrawler import SimpleCrawler


#class MyHTMLParser(HTMLParser):
#
#   def handle_starttag(self, tag, attrs):
#        print "Encountered the beginning of a %s tag" % tag
#
#    def handle_endtag(self, tag):
#        print "Encountered the end of a %s tag" % tag

p = SimpleCrawler()

f = urllib.urlopen('http://www.iciba.com/')
headers = f.info()
print 'Length: ', headers['Content-Length']

data = f.read()
p.feed(data)

f.close(  )
print "============WEB PAGE OUT LINKS=============="
for url in p.anchorlist:
    pieces = urlparse.urlparse(url)

    temp, fragment = urlparse.urldefrag(url)
    temp = urlparse.urljoin('http://www.iciba.com/',temp)
    parsedurl = urlparse.urlparse(temp)
    print urlparse.urlunparse(parsedurl)
print "==============IMAGE OUT LINKS==============="
for imageurl in p.imagelinklist:
    temp, fragment = urlparse.urldefrag(imageurl)
    temp = urlparse.urljoin('http://www.iciba.com/',temp)
    parsedurl = urlparse.urlparse(temp)
    print urlparse.urlunparse(parsedurl)
