import sys
import pkgutil
import encodings
import os
from socket import *

serverName = '127.0.0.1'
Port = int(sys.argv[1])

def all_encodings():
    modnames = set([modname for importer, modname, ispkg in pkgutil.walk_packages(
        path=[os.path.dirname(encodings.__file__)], prefix='')])
    aliases = set(encodings.aliases.aliases.values())
    return modnames.union(aliases)

print("Testing started...\n")

def makeTestreq(method,url,port,body=''):
    log = str(method) +' '+url+' HTTP/1.1'+"\r\n"
    h = str(method) +' '+url+' HTTP/1.1'+"\r\n"
    h+= "Host: localhost:"+str(port)+"\r\n"
    h+= 'Connection: keep-alive'+"\r\n"
    h+='User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'+"\r\n"
    h+='Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'+"\r\n"
    h+='Sec-Fetch-Site: none'+"\r\n"
    h+='Sec-Fetch-Mode: navigate'+"\r\n"
    h+='Sec-Fetch-User: ?1'+"\r\n"
    h+='Sec-Fetch-Dest: document'+"\r\n"
    h+='Accept-Encoding: gzip, deflate, br'+"\r\n"
    h+='Accept-Language: en-GB,en-US;q=0.9,en;q=0.8'+"\r\n"
    if body:
        h+="\r\n"+str(body)+"\r\n"
    return h , log

def Test(h,name,exStatus):
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,Port))
    clientSocket.send(h.encode())
    response = clientSocket.recv(1024)
    try:
        data = response.decode()
    except UnicodeDecodeError:
        data= response.decode("utf-8", "replace")
    status = data.split("\r\n")[0].split(" ")[1] 
    print("--->",purpose,status)   
    if exStatus == int(status):
        print("Test sucessfull ",name)  
    else:
        print("Unsuccessful",name)  

    clientSocket.close()

h , name  = makeTestreq("GET","/",Port)
exStatus  = 200
purpose = "Simple GET request"
Test(h,name,exStatus)

h , name  = makeTestreq("GET","/chef.jpg",Port)
exStatus = 200
purpose = "GET request for image"
Test(h,name,exStatus)

h , name  = makeTestreq("GET","/clay.mp3",Port)
exStatus = 200
purpose = "GET request for mp3"
Test(h,name,exStatus)

h , name  = makeTestreq("GET","/favicon.ico",Port)
exStatus = 200
purpose = "GET request for favicon.ico"
Test(h,name,exStatus)

h , name  = makeTestreq("GET","/home.html",Port)
exStatus = 200
purpose = "GET request for home.html"
Test(h,name,exStatus)

h , name  = makeTestreq("GET","/example.txt",Port)
exStatus = 200
purpose = "GET request for txt file"
Test(h,name,exStatus)

h , name  = makeTestreq("GET","/random",Port)
exStatus = 404
purpose = "Random GET request "
Test(h,name,exStatus)

h , name  = makeTestreq("GET","/random",Port)
exStatus = 404
purpose = "Random GET request "
Test(h,name,exStatus)

# h , name  = makeTestreq("POST","/random",Port)
# exStatus = 404
# purpose = "Random GET request "
# Test(h,name,exStatus)