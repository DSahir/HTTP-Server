import os , json , urllib.parse, uuid ,re,hashlib
from email.utils import formatdate
from helper import *
from datetime import datetime
now = datetime.now() 

statusCodesDic = {"101": "Switching Protocols","200": "OK","201": "Created","202": "Accepted","203": "Non-Authoritative Information","204": "No Content","205": "Reset Content","206": "Partial Content","300": "Multiple Choices","301": "Moved Permanently","302": "Found","303": "See Other","304": "Not Modified","305": "Use Proxy","307": "Temporary Redirect","400": "Bad Request","401": "Unauthorized","402": "Payment Required","403": "Forbidden","404": "Not Found","405": "Method Not Allowed","406": "Not Acceptable","407": "Proxy Authentication Required","408": "Request Time-out","409":" Conflict","410":" Gone","411":" Length Required","412":" Precondition Failed","413":" Request Entity Too Large","414":" Request-URI Too Large","415":" Unsupported Media Type","416":" Requested range not satisfiable","417":" Expectation Failed","500": "Internal Server Error","501": "Not Implemented","502": "Bad Gateway","503": "Service Unavailable","504": "Gateway Time-out","505": "HTTP Version not supported"}
ContentTypeDict = {"_xmlform":"application/x-www-form-urlencoded","_form":"multipart/form-data",".js":"text/javascript",".ogg":"application/ogg",".pdf":"application/pdf",".xhtml":"application/xhtml+xml",".json":"application/json",".zip":"application/zip",".mp3":"audio/mpeg",".mpeg":"audio/mpeg",".wav":"audio/x-wav",".gif":"image/gif",".jpg":"image/jpeg",".jpeg":"image/jpeg",".png":"image/png",".tiff":"image/tiff",".ico":"image/x-icon",".svg":"image/svg+xml",".css":"text/css",".csv":"text/csv",".html":"text/html",".txt":"text/plain",".xml":"text/xml",".mpeg":"video/mpeg",".mp4":"video/mp4",".wmv":"video/x-ms-wmv",".flv":"video/x-flv",".webm":"video/webm"}
postURI = ['/logs/access_log','/logs/error_log','/index.html','/templates/','/home.html']
delRestrict = [os.getcwd(),os.getcwd()+"/",os.getcwd()+"/logs/access_log" , os.getcwd()+"/logs/error_log" , os.getcwd()+"/Postdata.txt" ]

def GET(reqHeaderDict):

    resbody,StatusCode= isStatus406(reqHeaderDict)

    if StatusCode == 406:
        addlog(reqHeaderDict['Host'],"GET",406,reqHeaderDict['URI'])
        return StatusCode, "text/html", resbody    
    elif reqHeaderDict['URI'] == '/':
        resbody = HtmlResponse('./templates/index.html')   
        statusCode = 200 
    elif reqHeaderDict['URI'] == '/secret.html':
        resbody = 'Forbidden Page'.encode()
        statusCode = 403
    elif reqHeaderDict['URI'] == "/favicon.ico":
        resbody =  HtmlResponse("icons8-puzzle-40.png")
        statusCode = 200
        addlog(reqHeaderDict['Host'],"GET",statusCode,reqHeaderDict['URI'])
        return 200,"image/x-icon", resbody
    
    elif isExist(reqHeaderDict['absURI']):
        if isReadable(reqHeaderDict['absURI']):
            statusCode= 200
            resbody = HtmlResponse(reqHeaderDict['absURI'])
        else :
            statusCode = 401
            resbody='<html><body><center><h2 style="color:red;">ACCESS DENIED.</h2><br>PLEASE GO BACK.</center></body></html>'.encode()
        
    elif not isExist(reqHeaderDict['absURI']):
        statusCode = 404
        resbody = HtmlResponse("./templates/404.html")
    else:
        pass

    for k in ContentTypeDict:
        if k in reqHeaderDict['URI']:
            contentType = ContentTypeDict[k]
            addlog(reqHeaderDict['Host'],"GET",statusCode,reqHeaderDict['URI'])
            return statusCode,contentType, resbody
        else:
            contentType = 'text/html'

    addlog(reqHeaderDict['Host'],"GET",statusCode,reqHeaderDict['URI'])
    return statusCode,contentType, resbody

# DELETE Code
def DELETE(reqHeaderDict):
    File = reqHeaderDict['absURI']
    if File in delRestrict:
        statusCode=405
        contentType = "text/html"
        addlog (reqHeaderDict['Host'],"DELETE",statusCode,reqHeaderDict['URI'])
        resbody='<html><body><center><h2 style="color:red;">DELETE NOT ALLOWED!</h2></center></body></html>'.encode()
        return statusCode, contentType, resbody

    if os.access(File, os.F_OK):
        os.remove(File)
        statusCode=200
        contentType = "text/html"
        resbody='<html><body><center><h2 style="color:green;">File Deleted.</h2></center></body></html>'.encode()
        addlog(reqHeaderDict['Host'],"DELETE",statusCode,reqHeaderDict['URI'])
        return statusCode,contentType,resbody
    else:
        resbody=HtmlResponse("./templates/404.html")
        statusCode=404
        contentType="text/html"
        addlog(reqHeaderDict['Host'],"DELETE",statusCode,reqHeaderDict['URI'])       
    return statusCode,contentType, resbody


#POST
def POST(reqHeaderDict):
    reqType = reqHeaderDict["Content-Type"] if reqHeaderDict["Content-Type"] else "text/html"
    reqBody = reqHeaderDict["reqBody"] if  reqHeaderDict["reqBody"] else ""
    uri = reqHeaderDict["URI"]
    Path = reqHeaderDict["absURI"] 

    if uri in postURI:
        statusCode=405
        contentType = "text/html"
        addlog (reqHeaderDict['Host'],"POST",statusCode,reqHeaderDict["URI"])
        resbody='<html><body><center><h2 style="color:red;">ABRUPT POST REQUEST NOT ALLOWED!</h2></center></body></html>'.encode()
        return statusCode, contentType, resbody
    
    resbody,StatusCode= isStatus406(reqHeaderDict)
    if StatusCode == 406:
        addlog(reqHeaderDict['Host'],"POST",406,reqHeaderDict['URI'])
        return StatusCode, "text/html", resbody    

    for k,v in ContentTypeDict.items():
        if k in reqHeaderDict['URI'] and v in reqHeaderDict['Content-Type']:
            chk = Path 
            name = chk.split("/")[-1]
            break
        else:
            try:
                ext = reqHeaderDict['Content-Type'].split(";")[0]
            except:
                ext = reqHeaderDict['Content-Type'] 
            chk = Path + list(ContentTypeDict.keys())[list(ContentTypeDict.values()).index(ext)]
            name = chk.split("/")[-1] 

    if isExist(chk):
        statusCode=200
        contentType = "text/html"
        resbody='<html><body><center><h2 style="color:red;">File already exsits. <br> Make a PUT request.</h2></center></body></html>'.encode()
        addlog(reqHeaderDict['Host'],"POST",statusCode,reqHeaderDict['URI'])
        return statusCode, contentType, resbody
    
    else:
        if reqType == "text/plain":
            if not uri == '/':
                makePost(chk,reqBody)
                statusCode = 201         
                resbody = HtmlResponse("./templates/201.html")
                addlog(reqHeaderDict['Host'],"POST",statusCode,reqHeaderDict['URI'])
                contentType="text/html"
                return statusCode, contentType, resbody      
            else:        
                statusCode = 201         
                resbody = HtmlResponse("./templates/201.html")
                uid = str(uuid.uuid4())[:8]
                addlog(reqHeaderDict['Host'],"POST",statusCode,reqHeaderDict['URI'],uid)
                addPost(uid,reqBody)
                contentType="text/html"
                return statusCode, contentType, resbody

        elif "multipart/form-data" in reqType:            
            form = formToDict(reqHeaderDict)
            if  '/post1.html' in reqHeaderDict['URI']:
                dirname = os.getcwd() + "/post1/"
                filename = form['username']
                try:
                    with open(dirname + filename, 'w') as file:
                        file.write(json.dumps(form)) # use `json.loads` to do the reverse
                        file.close()
                        contentType = "text/html"
                        
                        resbody = HtmlResponse("./templates/201.html")
                        statusCode = 201
                        addlog(reqHeaderDict['Host'],"POST",statusCode,reqHeaderDict['URI'])                           
                except:
                    resbody = HtmlResponse("./templates/400.html")
                    statusCode = 400
                    contentType = "text/html"
                finally:    
                    return statusCode, contentType, resbody
            else:
                dirname = os.getcwd() + "/postForm/"
                filename = name or str(uuid.uuid4())[:8]
                try:
                    with open(dirname + filename, 'w') as file:
                        file.write(json.dumps(form)) # use `json.loads` to do the reverse
                        file.close()
                        resbody = HtmlResponse("./templates/201.html")
                        statusCode = 201
                        addlog(reqHeaderDict['Host'],"POST",statusCode,reqHeaderDict['URI'])
                        contentType = "text/html"
                        return statusCode, contentType, resbody
                except:
                    resbody = HtmlResponse("./templates/400.html")
                    statusCode = 400
                    contentType = "text/html"
                    return statusCode, contentType, resbody
        elif reqType == 'application/x-www-form-urlencoded':
            formxml = xmlformToDict(reqBody)
            dirname = os.getcwd() + "/xmlForm/"
            filename = name or str(uuid.uuid4())[:8]        
            try:
                with open(dirname + filename, 'w') as file:
                    file.write(json.dumps(formxml))
                    file.close()
                    resbody = HtmlResponse("./templates/201.html")
                    statusCode = 201
                    addlog(reqHeaderDict['Host'],"POST",statusCode,reqHeaderDict['URI'])
                    contentType = "text/html"
                    return statusCode, contentType, resbody
            except:
                resbody = HtmlResponse("./templates/400.html")
                statusCode = 400
                contentType = "text/html"
                return statusCode, contentType, resbody


# PUT Code
def PUT(reqHeaderDict):
    
    reqType = reqHeaderDict["Content-Type"] if reqHeaderDict["Content-Type"] else "text/html"
    reqBody = reqHeaderDict["reqBody"] if  reqHeaderDict["reqBody"] else ""
    uri = reqHeaderDict["URI"]
    Path = reqHeaderDict["absURI"] 

    if uri in postURI:
        statusCode=405
        contentType = "text/html"
        addlog (reqHeaderDict['Host'],"PUT",statusCode,uri)
        resbody='<html><body><center><h2 style="color:red;">ABRUPT PUT REQUEST NOT ALLOWED!</h2></center></body></html>'.encode()
        return statusCode, contentType, resbody
    
    resbody,StatusCode= isStatus406(reqHeaderDict)
    if StatusCode == 406:
        addlog(reqHeaderDict['Host'],"PUT",406,reqHeaderDict['URI'])
        return StatusCode, "text/html", resbody    

    for k,v in ContentTypeDict.items():
        if k in reqHeaderDict['URI'] and v in reqHeaderDict['Content-Type']:
            chk = Path 
            name = chk.split("/")[-1]
            break
        else:
            try:
                ext = reqHeaderDict['Content-Type'].split(";")[0]
            except:
                ext = reqHeaderDict['Content-Type'] 
            chk = Path + list(ContentTypeDict.keys())[list(ContentTypeDict.values()).index(ext)]
            name = chk.split("/")[-1] 

    
    if not uri == '/' :
        if not isExist(chk):
            if reqType == "text/plain":
                makePost(chk,reqBody)
            elif "multipart/form-data" in reqType:
                form = formToDict(reqHeaderDict)                
                dirname = os.getcwd() + "/postForm/"
                filename = name or str(uuid.uuid4())[:8]
                try:
                    with open(dirname + filename, 'w') as file:
                        file.write(json.dumps(form)) # use `json.loads` to do the reverse
                        file.close()
                        resbody = HtmlResponse("./templates/201.html")
                        statusCode = 201
                        contentType = "text/html"
                        addlog(reqHeaderDict['Host'],"PUT",statusCode,reqHeaderDict['URI'])
                        return statusCode, contentType, resbody
                except:
                    resbody = HtmlResponse("./templates/400.html")
                    statusCode = 400
                    contentType = "text/html"
                    addlog(reqHeaderDict['Host'],"PUT",statusCode,reqHeaderDict['URI'])
                    return statusCode, contentType, resbody

            elif reqType == 'application/x-www-form-urlencoded':
                formxml = xmlformToDict(reqBody)
                dirname = os.getcwd() + "/xmlForm/"
                filename = name or str(uuid.uuid4())[:8]        
                try:
                    with open(dirname + filename, 'w') as file:
                        file.write(json.dumps(formxml))
                        file.close()
                        resbody = HtmlResponse("./templates/201.html")
                        statusCode = 201
                        addlog(reqHeaderDict['Host'],"PUT",statusCode,reqHeaderDict['URI'])
                        contentType = "text/html"
                        return statusCode, contentType, resbody
                except:
                    resbody = HtmlResponse("./templates/400.html")
                    statusCode = 400
                    contentType = "text/html"
                    return statusCode, contentType, resbody

            statusCode=201
            contentType = "text/html"
            resbody='<html><body><center><h2 style="color:green;">New File Created.</h2></center></body></html>'.encode()
            addlog(reqHeaderDict['Host'],"PUT",statusCode,reqHeaderDict['URI'])
            return statusCode, contentType, resbody
        
        else:
            if reqType == "text/plain":
                if isWritable(chk):
                    fp = open(chk,"w")
                    fp.write(reqBody)
                    fp.close()
                    statusCode = 204         
                    resbody = HtmlResponse("./templates/204.html")
                    addlog(reqHeaderDict['Host'],"PUT",statusCode,reqHeaderDict['URI'])
                    contentType="text/html"
                    return statusCode, contentType, resbody
                else:
                    statusCode = 401        
                    resbody = HtmlResponse("./templates/401.html")
                    addlog(reqHeaderDict['Host'],"PUT",statusCode,reqHeaderDict['URI'])
                    contentType="text/html"
                    return statusCode, contentType, resbody
            elif "multipart/form-data" in reqType:
                if isWritable(chk):
                    form = formToDict(reqHeaderDict)
                    
                    try:
                        with open(chk, 'w') as file:
                            file.write(json.dumps(form)) # use `json.loads` to do the reverse
                            file.close()
                            contentType = "text/html"
                            statusCode = 204         
                            resbody = HtmlResponse("./templates/204.html")
                        
                    except:
                        resbody = HtmlResponse("./templates/400.html")
                        statusCode = 400
                        contentType = "text/html"
                    finally:    
                        addlog(reqHeaderDict['Host'],"PUT",statusCode,reqHeaderDict['URI'])
                        return statusCode, contentType, resbody                   
                    
                else:
                    statusCode = 401        
                    resbody = HtmlResponse("./templates/401.html")
                    addlog(reqHeaderDict['Host'],"PUT",statusCode,reqHeaderDict['URI'])
                    contentType="text/html"
                    return statusCode, contentType, resbody
            elif reqType == 'application/x-www-form-urlencoded':
                if isWritable(chk):
                    formxml = xmlformToDict(reqBody)
                    
                    try:
                        with open(chk, 'w') as file:
                            file.write(json.dumps(formxml))
                            file.close()
                            contentType = "text/html"
                            statusCode = 204         
                            resbody = HtmlResponse("./templates/204.html")
                        
                    except:
                        resbody = HtmlResponse("./templates/400.html")
                        statusCode = 400
                        contentType = "text/html"
                    finally:    
                        addlog(reqHeaderDict['Host'],"PUT",statusCode,reqHeaderDict['URI'])
                        return statusCode, contentType, resbody                   
                    
                else:
                    statusCode = 401        
                    resbody = HtmlResponse("./templates/401.html")
                    addlog(reqHeaderDict['Host'],"PUT",statusCode,reqHeaderDict['URI'])
                    contentType="text/html"
                    return statusCode, contentType, resbody
            else: 
                if isWritable(chk):
                    fp = open(chk,"w")
                    fp.write(reqBody)
                    fp.close()
                    statusCode = 204         
                    resbody = HtmlResponse("./templates/204.html")
                    addlog(reqHeaderDict['Host'],"PUT",statusCode,reqHeaderDict['URI'])
                    contentType="text/html"
                    return statusCode, contentType, resbody
                else:
                    statusCode = 401        
                    resbody = HtmlResponse("./templates/401.html")
                    addlog(reqHeaderDict['Host'],"PUT",statusCode,reqHeaderDict['URI'])
                    contentType="text/html"
                    return statusCode, contentType, resbody   
    elif uri == '/':
        if reqType == "text/plain":
            statusCode = 201         
            resbody = HtmlResponse("./templates/201.html")
            uid = str(uuid.uuid4())[:8]
            addlog(reqHeaderDict['Host'],"PUT",statusCode,reqHeaderDict['URI'],uid)
            addPost(uid,reqBody)
            contentType="text/html"
            return statusCode, contentType, resbody

        elif "multipart/form-data" in reqType:            
            form = formToDict(reqHeaderDict)
            dirname = os.getcwd() + "/postForm/"
            filename = name or str(uuid.uuid4())[:8]

            try:
                with open(dirname + filename, 'w') as file:
                    file.write(json.dumps(form)) # use `json.loads` to do the reverse
                    file.close()
                    resbody = HtmlResponse("./templates/201.html")
                    statusCode = 201
                    addlog(reqHeaderDict['Host'],"PUT",statusCode,reqHeaderDict['URI'])
                    contentType = "text/html"
                    return statusCode, contentType, resbody
            except:
                resbody = HtmlResponse("./templates/400.html")
                statusCode = 400
                contentType = "text/html"
                return statusCode, contentType, resbody
                
        elif reqType == 'application/x-www-form-urlencoded':
            formxml = xmlformToDict(reqBody)
            dirname = os.getcwd() + "/xmlForm/"
            filename = name or str(uuid.uuid4())[:8]        
            try:
                with open(dirname + filename, 'w') as file:
                    file.write(json.dumps(formxml))
                    file.close()
                    resbody = HtmlResponse("./templates/201.html")
                    statusCode = 201
                    addlog(reqHeaderDict['Host'],"PUT",statusCode,reqHeaderDict['URI'])
                    contentType = "text/html"
                    return statusCode, contentType, resbody
            except:
                resbody = HtmlResponse("./templates/400.html")
                statusCode = 400
                contentType = "text/html"
                return statusCode, contentType, resbody
        else:
            resbody = HtmlResponse("./templates/400.html")
            statusCode = 400
            contentType = "text/html"
            return statusCode, contentType, resbody