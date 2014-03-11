import httplib,urllib

def get_status_code(host, path="/"):
    """ This function retreives the status code of a website by requesting
        HEAD data from the host. This means that it only requests the headers.
        If the host cannot be reached or something else goes wrong, it returns
        None instead.
    """
    try:
        conn = httplib.HTTPConnection(host)
        conn.request("HEAD", path)
        return conn.getresponse().status
    except StandardError:
        return None

def get_HttpResponse(host):
    try:
        conn = httplib.HTTPConnection(host)
        conn.request()
        return conn.getresponse()
    except StandardError:
        return None
    

#print get_status_code("www.google.com") # prints 200
#print get_status_code("www.google.com", "/nonexistant") # prints 404
#print get_HttpResponse("www.google.com")
conn=httplib.HTTPConnection('dev11.targetecrf.com')
#conn=httplib.HTTPConnection('www.google.com')
conn.set_debuglevel(1)
#conn.request("GET","")
params=urllib.urlencode({'txtUsername':'websiteadmin1','USMPWD':'target1'})
conn.request("POST","/Account/Login.aspx?",params)
#conn.request("GET","")
r1=conn.getresponse()

print r1.version
print r1.status, r1.reason
print r1.msg
print "===="
print r1.fileno()
print "====content==="
print r1.read()

