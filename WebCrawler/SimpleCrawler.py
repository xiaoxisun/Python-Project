import formatter
import Queue
import urlparse, urllib
import robotparser
import warnings
import os
import htmllib
import time

from uniwebsearch import google

##
##a = SimpleCrawler.SimpleCrawler('china')


class ExtendedHTMLParser(htmllib.HTMLParser):
    """This is a simple crawler that is inherited from htmllib.HTMLParser.

    The part of processing anchor elements is little changed.
    However, the class deals with image elements to extract potential 'src'
    attributes as outer links

    """
    def __init__(self, verbose=0):
        htmllib.HTMLParser.__init__(self, formatter.NullFormatter(  ), verbose)
        self.m_imagelinklist = []

        

    def handle_image(self, src, alt, *args):
        """This overrided method deals with image elements appeared in a page.

        If there is a src attribute, add its corresponding url into imagelinklist

        """
        if src:
            self.m_imagelinklist.append(src)

class CrawlingURL:
    def __init__(self, url, depth):
        self.m_url = url
        self.m_depth = depth

class SimpleCrawler:
    def __init__(self, keywords, n = 100, outputfilename = 'output.txt'):
        self.m_seen = {}# record seen URLs
        self.m_disallowURL = {}# record website whose pages are not allowed from crawler
        self.m_allowallURL = {}# record website whose pages are allowed from crawler
        self.m_crawling = Queue.Queue(-1) #the size of queue is ifinite
        self.m_keywords = keywords
        self.m_num = n
        self.m_crawledbytes = 0 #number of bytes the crawler downloaded
        self.m_num_urls = 0 #number of urls the crawler encountered
        self.m_outputfile = outputfilename
        

        #open the output files
        try:
            self.file = open(self.m_outputfile, 'w')
            self.imagefile = open('images.txt', 'w')
            self.plotfile = open('plots.txt', 'w')
            self.IOsucess = True
        except IOError, e:
            print e
            self.IOsucess = False
            self.mf_terminate_file()

        print "START CRAWLING NOW..."
        
        #get start URL to be parsed
        for (name, url, desc) in google(self.m_keywords, 10):

            encounteredURL = CrawlingURL(url,-1)

            self.mf_process_urls(encounteredURL, encounteredURL)

        #start to parse URLs
        self.mf_parse_url()
        #All done. Terminate.
        self.mf_terminate_file()

    def mf_terminate_file(self):
        if(self.IOsucess):
            try:
                self.file.close()
                self.imagefile.close()
                self.plotfile.close()
                print "Successfully close the output file."
            except IOError, e:
                print e
        else:
            print "Cannot Open Output File"

    def myurlopen(self,url,data = None, proxies = None):
        #/////////////
        # Shortcut for basic usage
        _urlopener = None
        """Create a file-like object for the specified URL to read from."""
        from warnings import warnpy3k
        warnings.warnpy3k("urllib.urlopen() has been removed in Python 3.0 in "
                            "favor of urllib2.urlopen()", stacklevel=2)

        
        if proxies is not None:
            opener = myURLopener(proxies=proxies)
        elif not _urlopener:
            opener = myURLopener()
            _urlopener = opener
        else:
            opener = _urlopener
        if data is None:
            return opener.open(url)
        else:
            return opener.open(url, data)
        #////////////////

    def mf_parse_url(self):
        """
        Do parsing until the queue is empty or reach the max number of URLs to be crawled
        """
        while True:
            if (self.m_crawling.qsize() <= 0) or (self.m_num_urls > self.m_num):
                print "Terminate Crawling..."
                print "Number of bytes downloaded: ", self.m_crawledbytes
                print "Number of URL in the crawling queue: ", self.m_crawling.qsize()
                print "Number of URL parsed: ", self.m_num_urls

                self.file.write("==============================================\n")
                self.file.write("==============================================\n")
                self.file.write("Statistical Statements\n")
                self.file.write("Number of bytes downloaded: " + str(self.m_crawledbytes) + "\n")
                self.file.write("Number of URLs in the crawling queue: " + str(self.m_crawling.qsize()) + "\n")
                self.file.write("Number of URLs parsed: " + str(self.m_num_urls) + "\n")
                break
            
            p = ExtendedHTMLParser()
            
            baseurl = self.m_crawling.get()
            
            print "---START ANOTHER PAGE---"

            print "Current URL: ", baseurl.m_url
            

            self.file.write("Current URL: " + baseurl.m_url + "\n")
            
            
            
            try:
                
                #open the URL
                f = self.myurlopen(baseurl.m_url)
                #get status code and print it on screen and into file
                print f.code
                self.file.write("Status Code: " + str(f.code) + "\n")
                
                #if this url has an alias, label this alias as seen too
                currenturl = f.geturl()
                if baseurl.m_url <> currenturl:
                    baseurl.m_url = currenturl
                    self.m_seen[baseurl.m_url] = baseurl.m_depth

                    print "Redirected URL: ", baseurl.m_url
                    self.file.write("Redirected URL: " + baseurl.m_url + "\n")

                print "Depth of this URL: ", baseurl.m_depth
                self.file.write("Depth of this URL: " + str(baseurl.m_depth) + "\n")
            
                #get header information
                headers = f.info()
                
                print headers

                #if there is content length in the header
                if headers.has_key('Content-Length'):
                    #extract it
                    pagelength = headers['Content-Length']
                    
                else:
                    #otherwise, extract it from file attribute
                    filename, filepageheader = urllib.urlretrieve(baseurl.m_url,'tempt')
                    print filename
                    statinfo = os.stat(filename)
                    pagelength = statinfo.st_size
                    
                self.file.write("Page Length (Bytes): " + str(pagelength) +"\n")
                                            
                #if the page type is labelled as text/...
                if headers.has_key('Content-Type'):
                    if headers['Content-Type'].startswith('text'):

                        #update number of URLs that have been crawled
                        self.m_num_urls = self.m_num_urls + 1    

                        #update the number of bytes the crawler downloaded
                    
                        self.m_crawledbytes = int(self.m_crawledbytes) + int(pagelength)

                        try:
                            data = f.read()
                            p.feed(data)
                            f.close()
                        except htmllib.HTMLParseError, e:
                            print e
                            self.file.write("HTML Parse Error on this page")
                            self.file.write("at: " + time.strftime('%X %x') + "\n")
                            self.file.write("---------------------------------------\n")
                            continue
                        self.plotfile.write(str(pagelength) + " " + str(self.m_crawledbytes) + " " + str(time.time()) + " " + str(self.m_crawling.qsize()) + "\n")
                        self.file.write("at: " + time.strftime('%X %x') + "\n")
                        self.file.write("---------------------------------------\n")
                        print self.m_num_urls
                        print self.m_crawling.qsize()
                        for url in p.anchorlist:
                            encounteredURL = CrawlingURL(url,-1)
                            self.mf_process_urls(baseurl, encounteredURL)
                        for image in p.m_imagelinklist:
                            encounteredURL = CrawlingURL(image,-1)
                            self.mf_process_urls(baseurl, encounteredURL)

                else:
                    print "No Content Type...skip"
                    self.file.write("No Content Type...skip\n")
                    continue
                #otherwise, do not parse this page
                if headers['Content-Type'].startswith('image'):
                    print "!Image URL: " + baseurl.m_url
                    self.file.write("Images encounted. Do not parse it but output its URL into images.txt\n")
                    self.file.write("---------------------------------------\n")
                    self.imagefile.write("Image URL: " + baseurl.m_url + "\n")
                    self.imagefile.write("---------------------------------------\n")
                if headers['Content-Type'].startswith('message'):
                    print "!Message URL: " + baseurl.m_url
                if headers['Content-Type'].startswith('multipart'):
                    print "!Multipart URL: " + baseurl.m_url
                if headers['Content-Type'].startswith('video'):
                    print "!Video URL: " + baseurl.m_url
                if headers['Content-Type'].startswith('application'):
                    print "!Application URL: " + baseurl.m_url
                if headers['Content-Type'].startswith('audio'):
                    print "!Audio URL: " + baseurl.m_url

                
            except IOError, e:
                print e
                continue    #if there is some error when open a URL
                            #parse the next URL
    
    def mf_process_urls(self, baseurl, encounteredurl):
        """parse this url

        Record the depth of this URL.
        Only push reasonable URL into the crawling queue
        
        """

        #first, parse relative url and fragment
        tempurl, fragment = urlparse.urldefrag(encounteredurl.m_url)
        tempurl = urlparse.urljoin(baseurl.m_url, tempurl)

        #check if there is a robot.txt
        robottext = urlparse.urljoin(baseurl.m_url,'///') + 'robot.txt'

        allowall = False
        if self.m_disallowURL.has_key(robottext):
            
            #print "Disallow All!"
            return
        elif self.m_allowallURL.has_key(robottext):
            allowall = True
            #print "Allow ALL!"
        else:
            rp = ExtendedRobotFileParser(robottext)
            #rp.set_url(robottext)
            rp.read()
            if rp.disallow_all == True:
                self.m_disallowURL[robottext] = "robot"
                
            if rp.allow_all == True:
                allowall = True
                self.m_allowallURL[robottext] = "robot"
            
                    
        #check if it is a reasonable url
        #Although it could be checked by TRY-EXCEPTION clauses, eliminating
        #some common scheme could speed up the processing
        parsedurl = urlparse.urlparse(tempurl)
        newencounteredURL = CrawlingURL(tempurl, int(baseurl.m_depth)+1)
        if not self.m_seen.has_key(newencounteredURL.m_url):
            if parsedurl[0] == 'mailto':
                print "===Encounter mailto in attribute src...skip"
                self.m_seen[tempurl] = -1
            elif parsedurl[0] == 'javascript':
                print "===Encounter javascript in attribute src...skip"
                self.m_seen[tempurl] = -1
            elif parsedurl[0] == 'irc':
                print "===Encounter Internet Relay Chat...skip"
                self.m_seen[tempurl] = -1
            elif (allowall == False) and (not rp.can_fetch("*",tempurl)):
                print "===Disallowed by robot.txt...skip. The URL is " + tempurl
                self.m_seen[tempurl] = -1
            #if it is a reasonable url
            else:
            
            #if not self.m_seen.has_key(newencounteredURL.m_url):
                #If has not seen this url, label it as seen,
                #and push it into queue
                self.m_crawling.put(newencounteredURL)
                #print self.m_crawling
                self.m_seen[newencounteredURL.m_url] = newencounteredURL.m_depth


class myURLopener(urllib.FancyURLopener):

    def http_error_401(self, url, fp, errcode, errmsg, headers, data=None):
        return None	# do nothing


class ExtendedRobotFileParser(robotparser.RobotFileParser):

    def myurlopen(self,url,data = None, proxies = None):
        #/////////////
        # Shortcut for basic usage
        _urlopener = None
        """Create a file-like object for the specified URL to read from."""
        from warnings import warnpy3k
        warnings.warnpy3k("urllib.urlopen() has been removed in Python 3.0 in "
                            "favor of urllib2.urlopen()", stacklevel=2)

        
        if proxies is not None:
            opener = myURLopener(proxies=proxies)
        elif not _urlopener:
            opener = myURLopener()
            _urlopener = opener
        else:
            opener = _urlopener
        if data is None:
            return opener.open(url)
        else:
            return opener.open(url, data)
        #////////////////
        
    def read(self):
        """Reads the robots.txt URL and feeds it to the parser.
            Most of the codes are inherited from base class,
            except that are specified
        """
        existed = False
        try:
            #f = self.myurlopen(self.url)
            opener = robotparser.URLopener()
            f = opener.open(self.url)
            #if this url has an alias, label this alias as seen too
            currenturl = f.geturl()
            if (currenturl == self.url) and f.code == 200 :
                existed = True
            else:
                existed = False
            f.close()
        except IOError, e:
            existed = False
        
        #if robot.txt does exist, do the parsing
        if existed == True:
            opener = robotparser.URLopener()
            f = opener.open(self.url)
            
                
            lines = [line.strip() for line in f]
        
            f.close()
            self.errcode = opener.errcode

            
            if self.errcode in (401, 403):
                self.disallow_all = True
            elif self.errcode >= 400:
                self.allow_all = True
            elif self.errcode == 200 and lines:
                self.parse(lines)
        else:
            self.allow_all = True
