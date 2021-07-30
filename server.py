
from threading import Thread
from socket import *
from time import mktime
from helper import *
from email.utils import formatdate
from config import *
from datetime import *
now = datetime.now()
from handle import *
import sys, os, time,mimetypes

def create_header(  statusCode, resbody , ContentType ="text/html" ,cookie=''):
    header =  ("HTTP/1.1 "+str(statusCode)+" "+str(statusCodesDic[str(statusCode)])+"\r\n")
    header += ("Date: " + str(now.strftime('%a, %d %b %Y %H:%M:%S'))+" IST"+"\r\n")    # Date in required rfc 1123 format
    header += ("Server: Dhanshri-Http-server \r\n")
    header += ("Connection: close\r\n")
    header += ("Content-Type: " + str(ContentType) + "; charset=UTF-8\r\n")
    header += ("Content-Length: "+str(len(resbody))+ "\r\n")
    if cookie:
        header += (str(cookie)+ "\r\n")    
    header += ("\r\n")
    return header

# Implementation of a simple queue
class Queue:
    def __init__(self):
        self.items = []
    def is_empty(self):
        return self.items == []
    def enqueue(self, item):
        self.items.insert(0, item)
    def dequeue(self):
        return self.items.pop()
    def size(self):
        return len(self.items)


# Safely prints to console without interruption
# Normal print is bad because implicit newline can cause a race condition with other print statements
def safeprint(output):
    printqueue.enqueue(output)

# Thread constantly checks if there's anything to print and prints it if so
def checkprint():
    while True:
        if not printqueue.is_empty():
            while not printqueue.is_empty():
                text = printqueue.dequeue()
                print(text, file=sys.stderr)


# If any thread has finished, remove it from the list
def checkthreads():
    while True:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)

# Handles a single request from a specific client, then closes
def handlerequest(connectionSocket):
    # Attempts to receive message, terminating process if it times out
    starttime = time.time()
    request = ""
    connectionSocket.setblocking(0)
    while request == "":
        
        if time.time() > starttime + TIMEOUT:
            safeprint("Error: socket recv timed out")
            connectionSocket.close()
            return
        try:
            recv = connectionSocket.recv(4096)
            try:
                request = recv.decode()
            except UnicodeDecodeError:
                request= recv.decode("utf-8", "replace")
        except error:
            pass
            
            

    # If end of data is hit while waiting for more input, terminate connection immediately
    if len(request) == 0 or "\r\n" not in request:
        safeprint("Error: unexpected end of input")
        connectionSocket.close()
        return

    # Split the request by spaces
    reqData = request.split("\r\n")
    reqHeaderDict = {}
    try:
        reqMethod = reqData[0].split()[0]
        reqHeaderDict.update({"reqMethod": reqMethod})
    except:
        pass
    try:
        URI = reqData[0].split()[1]
        absURI = os.getcwd() + URI
        reqHeaderDict.update({"URI": URI})
        reqHeaderDict.update({"absURI": absURI})
    except:
        pass
    for i in reqData[1:] :
        k = i.split(": ")[0]

        if k == '':
            k = "reqBody"
            body = ''.join(reqData[reqData.index(i):])
            reqHeaderDict.update({k : body})                
            break
        try:
            v = i.split(": ")[1]
        except:
            pass
        reqHeaderDict.update({k : v})
    
    reqHeaderDict.update({"URI": URI})
    reqHeaderDict.update({"absURI": absURI})
    print(reqHeaderDict)

    if "Cookie" in reqHeaderDict :
        if "sessionId" in reqHeaderDict["Cookie"]:
            c = reqHeaderDict["Cookie"].split("sessionId=")[-1]
            # print(c)
            if createCookie(c) :
                cookie,exp,cookieHead = setCookie()     
                appendCookie(str(cookie),str(exp))
            else:
                cookieHead='' 
                cookie=''   
        else:
            cookieHead=''
            cookie=''   
    else:
        cookie,exp,cookieHead = setCookie()         
        appendCookie(str(cookie),str(exp))
    print(cookie)
    # Get 
    if reqMethod == "GET":
        statusCode, contentType, resbody = GET(reqHeaderDict)
        header= create_header( statusCode, resbody ,contentType,cookieHead)
        output = header.encode() + resbody 

    # Post
    elif reqMethod == "POST":
        statusCode, contentType, resbody = POST(reqHeaderDict)
        header= create_header( statusCode, resbody ,contentType,cookieHead)
        output = header.encode() + resbody

    # Put
    elif reqMethod == "PUT":
        statusCode, contentType, resbody = PUT(reqHeaderDict)
        header= create_header( statusCode, resbody ,contentType,cookieHead)
        output = header.encode() + resbody

    #Delete
    elif reqMethod == "DELETE":
        statusCode,contentType, resbody = DELETE(reqHeaderDict)
        header= create_header( statusCode, resbody ,contentType )
        output = header.encode() + resbody
        
    # Head
    elif reqMethod == "HEAD":
        statusCode, contentType, resbody = GET(reqHeaderDict)
        header= create_header( statusCode, resbody ,contentType )
        output = header.encode()
    
    connectionSocket.sendall(output)
    connectionSocket.close()

# Port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
# maxrq = int(sys.argv[2]) if len(sys.argv) > 2 else MAXCONNECTIONS
# timeout = float(sys.argv[3]) if len(sys.argv) > 3 else TIMEOUT

# Create the main server socket (to listen for incoming connections) and bind server to the socket
serverSocket = socket(AF_INET, SOCK_STREAM)
threads = list()
printqueue = Queue()

def startserver(Port = PORT,maxrq = MAXCONNECTIONS,timeout=TIMEOUT):
    global serverSocket
    serverSocket.bind(('127.0.0.1', Port))
    print("HTTP server running on port:\n",Port)

    # Tell the OS this will be used as a passive socket (i.e., to receive incoming connections)
    serverSocket.listen(maxrq)

    # Set up printer thread
    global printqueue
    printer = Thread(target=checkprint, daemon=True)
    printer.start()

    # Must keep track of every thread currently running something, and when they die
    global threads
    deathchecker = Thread(target=checkthreads, daemon=True)
    deathchecker.start()

    while True:
        # Block waiting for incoming connections, then prints information about new socket
        connectionSocket, addr = serverSocket.accept()
        safeprint("Information: received new connection from %s, port %s" % (addr[0], addr[1]))

        # If there's space for a new connection, add it to the list of threads and start it
        if len(threads) < maxrq:
            newthread = Thread(target=handlerequest, args=(connectionSocket,), daemon=True)
            newthread.start()
            threads.append(newthread)
        # Otherwise, print error and kill the connection immediately
        else:
            safeprint("Error: too many requests")
            connectionSocket.close()
            continue

def stopserver ():
    global serverSocket
    serverSocket.close()