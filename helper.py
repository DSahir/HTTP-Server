import os , json , urllib.parse, uuid ,re,hashlib , random ,string
from email.utils import formatdate
from helper import *
from datetime import *
now = datetime.now()
from http import cookies



statusCodesDic = {"101": "Switching Protocols","200": "OK","201": "Created","202": "Accepted","203": "Non-Authoritative Information","204": "No Content","205": "Reset Content","206": "Partial Content","300": "Multiple Choices","301": "Moved Permanently","302": "Found","303": "See Other","304": "Not Modified","305": "Use Proxy","307": "Temporary Redirect","400": "Bad Request","401": "Unauthorized","402": "Payment Required","403": "Forbidden","404": "Not Found","405": "Method Not Allowed","406": "Not Acceptable","407": "Proxy Authentication Required","408": "Request Time-out","409":" Conflict","410":" Gone","411":" Length Required","412":" Precondition Failed","413":" Request Entity Too Large","414":" Request-URI Too Large","415":" Unsupported Media Type","416":" Requested range not satisfiable","417":" Expectation Failed","500": "Internal Server Error","501": "Not Implemented","502": "Bad Gateway","503": "Service Unavailable","504": "Gateway Time-out","505": "HTTP Version not supported"}
ContentTypeDict = {"_xmlform":"application/x-www-form-urlencoded","_form":"multipart/form-data",".js":"text/javascript",".ogg":"application/ogg",".pdf":"application/pdf",".xhtml":"application/xhtml+xml",".json":"application/json",".zip":"application/zip",".mp3":"audio/mpeg",".mpeg":"audio/mpeg",".wav":"audio/x-wav",".gif":"image/gif",".jpg":"image/jpeg",".jpeg":"image/jpeg",".png":"image/png",".tiff":"image/tiff",".ico":"image/x-icon",".svg":"image/svg+xml",".css":"text/css",".csv":"text/csv",".html":"text/html",".txt":"text/plain",".xml":"text/xml",".mpeg":"video/mpeg",".mp4":"video/mp4",".wmv":"video/x-ms-wmv",".flv":"video/x-flv",".webm":"video/webm"}
postURI = ['/logs/access_log','/logs/error_log','/index.html','/templates/','/home.html']
delRestrict = [os.getcwd(),os.getcwd()+"/",os.getcwd()+"/logs/access_log" , os.getcwd()+"/logs/error_log" , os.getcwd()+"/Postdata.txt" ]


def isStatus406 (reqHeaderDict):
    Code, resbody = None, None
    if 'Accept-Language' in reqHeaderDict:
        lang = reqHeaderDict['Accept-Language']
        if 'en' not in lang:
            Code = 406
            resbody = 'Server only works with english language.\n'.encode()
    return resbody , Code

def isReadable (file):
    return os.access(file, os.R_OK) # Check for read access
def isWritable(file):
    return os.access(file, os.W_OK) # Check for write access
def isExec(file):
    return os.access(file, os.X_OK) # Check for execution access
def isExist(file):
    return os.access(file, os.F_OK) # Check for existance of file

def HtmlResponse(file):
    f = open(file, 'rb')
    resbody = f.read()
    f.close()
    return resbody 

def addlog(host,method,code,uri='',uid='',user='-',assessid="-"):
    date = str(now.strftime("%m/%d/%Y %H:%M:%S")) +" IST"
        # date = str(formatdate(timeval=None, localtime=False, usegmt=True))  # Date in required rfc 1123 format
    if code >399:
        fp = open("./logs/error_log",'a')
        fp.write("127.0.0.1 "+user+" "+assessid+" ["+date+"] \""+method+" "+uri+" "+"HTTP/1.1\" "+str(code)+ " "+uid+"\n")
        fp.close()
    else:    
        fp = open("./logs/access_log",'a')
        fp.write("127.0.0.1 "+user+" "+assessid+" ["+date+"] \""+method+" "+uri+" "+"HTTP/1.1\" "+str(code)+ " "+uid+"\n")
        fp.close()


def appendCookie(c,exp):
    with open ("cookie.txt","a") as f:
        f.write(c+"="+str(exp)+"\n")
    f.close()

def createCookie(c):
    with open("cookie.txt", "r") as f:
        lines = f.readlines()
    f.close()
    found = False
    with open("cookie.txt", "w") as f:
        for line in lines:
            if str(c) in line:
                found = True
                t = datetime.strptime(line.split("=")[-1].split("\n")[0],'%a, %d %b %Y %H:%M:%S')
                # print("-->",t<now)
                if t < now:
                    
                    create = True
                else:
                    f.write(line) 
                    create = False
            else:
                found = False
                f.write(line)        
    f.close()
    if found:
        return True if create else False
    else:
        return True

def show_cookie(c):
    for key, morsel in c.items():
        for name in morsel.keys():
            if morsel[name] :
                return morsel.value, morsel[name]

def setCookie():
    c = cookies.SimpleCookie()
    # A cookie with a value that has to be encoded to fit into the header
    c['sessionId'] = ''.join(random.choice(string.ascii_lowercase) for i in range(4)) + str(random.randint(1,1000))+''.join(random.choice(string.ascii_lowercase) for i in range(3))
    # A cookie that expires  in 5 minutes
    # c['expires_at_time'] = 'cookie_value'
    time_to_live = timedelta(minutes=4)
    expires = (now + time_to_live)
    # Date format: Wdy, DD-Mon-YY HH:MM:SS GMT
    expires_at_time = expires.strftime('%a, %d %b %Y %H:%M:%S')
    c['sessionId']['expires'] = expires_at_time
    cookie,exp = show_cookie(c)
    return cookie ,exp,c

def addPost(uid,data):
    date = str(now.strftime("%m/%d/%Y %H:%M:%S")) +" IST"   # Date in required rfc 1123 format
    fp = open("Postdata.txt",'a')
    fp.write(uid+" "+ date+" "+ data+"\n")
    fp.close()

def makePost(file,data):
    fp = open(file,'w')
    fp.write(data)
    fp.close()

def formToDict(reqHeaderDict):
    boundary = reqHeaderDict['Content-Type'].split("boundary=")[1]
    lisis=[]
    for e in reqHeaderDict['reqBody'].split("--"+boundary)[1:-1]:
        lisis.append(e.split("=")[1])    
    form = {}
    for e in lisis:
        form[(urllib.parse.unquote(e.split('"')[1::2][0], encoding='utf-8', errors='replace'))] = (urllib.parse.unquote(e.split('"')[2::3][0], encoding='utf-8', errors='replace'))     # the [1::2] is a slicing which extracts odd values
    return form    

def xmlformToDict(reqBody):
    lis = reqBody.split("&")
    formxml={}
    for e in lis:
        formxml[(urllib.parse.unquote(e.split("=")[0], encoding='utf-8', errors='replace'))] = (urllib.parse.unquote(e.split("=")[1], encoding='utf-8', errors='replace'))
    return formxml        
