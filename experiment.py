# # # reqHeaderDict ={}
# # # ContentTypeDict = {'/':'text/html',".js":"application/javascript",".ogg":"application/ogg",".pdf":"application/pdf",".xhtml":"application/xhtml+xml",".json":"application/json",".zip":"application/zip",".mpeg":"audio/mpeg",".wav":"audio/x-wav",".gif":"image/gif",".jpg":"image/jpeg",".jpeg":"image/jpeg",".png":"image/png",".tiff":"image/tiff",".ico":"image/x-icon",".svg":"image/svg+xml",".css":"text/css",".csv":"text/csv",".html":"text/html",".txt":"text/plain",".xml":"text/xml",".mpeg":"video/mpeg",".mp4":"video/mp4",".wmv":"video/x-ms-wmv",".flv":"video/x-flv",".webm":"video/webm"}

# # # reqHeaderDict['URI'] = "chej.jpg"

# # '''
# # RFC 2616 also mentions the possibility of extension tokens, and these days most browsers recognise inline to mean you do want the entity displayed if possible (that is, if it's a type the browser knows how to display, otherwise it's got no choice in the matter). This is of course the default behaviour anyway, but it means that you can include the filename part of the header, which browsers will use (perhaps with some adjustment so file-extensions match local system norms for the content-type in question, perhaps not) as the suggestion if the user tries to save.

# # Hence:

# # Content-Type: application/octet-stream
# # Content-Disposition: attachment; filename="picture.png"
# # Means "I don't know what the hell this is. Please save it as a file, preferably named picture.png".

# # Content-Type: image/png
# # Content-Disposition: attachment; filename="picture.png"
# # Means "This is a PNG image. Please save it as a file, preferably named picture.png".

# # Content-Type: image/png
# # Content-Disposition: inline; filename="picture.png"


# # multipart/mixed
# # multipart/alternative
# # multipart/related (using by MHTML (HTML mail).)
# # multipart/form-data

# # ".xml":"application/xml"

# # '''

# # # dic = {'reqMethod': 'POST', 'URI': '/post1.html', 'absURI': '/home/dhanshri/Public/CN/http-win/Dhanshri/server/post1.html', 'Host': 'localhost:7001', 'Connection': 'keep-alive', 'Content-Length': '330', 'Cache-Control': 'max-age=0', 'Upgrade-Insecure-Requests': '1', 'Origin': 'http://localhost:7001', 'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryAJdiedyb5R0tdVlB', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-User': '?1', 'Sec-Fetch-Dest': 'document', 'Referer': 'http://localhost:7001/post1.html', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.9', 'Cookie': 'csrftoken=7TR4CPuayEP6lP0hWKKlEhuEuf9JWwFIqBmKnSl2E3QhZdtRr00gC0NQPbyUDtp6', 'reqBody': '------WebKitFormBoundaryAJdiedyb5R0tdVlBContent-Disposition: form-data; name="name"Dhanu------WebKitFormBoundaryAJdiedyb5R0tdVlBContent-Disposition: form-data; name="age"23------WebKitFormBoundaryAJdiedyb5R0tdVlBContent-Disposition: form-data; name="college"COEP------WebKitFormBoundaryAJdiedyb5R0tdVlB--'}

# # import json

# # # # as requested in comment
# # # exDict = {'exDict': 'Dhanu' , 'ahe'}

# # # with open('file.txt', 'w') as file:
# # #      file.write(json.dumps(exDict)) # use `json.loads` to do the reverse

# # import hashlib
# # hash_object = hashlib.sha256(b'Hello World')
# # hex_dig = hash_object.hexdigest()
# # print(hex_dig)


# # from http import cookies
# # import datetime,random,string

# # now = datetime.datetime.now()

# # def show_cookie(c):
#     # def show_cookie(c):
#     # print(c)
#     # for key, morsel in c.items():
#     #     print()
#     #     print('key =', morsel.key)
#     #     print('  value =', morsel.value)
#     #     print('  coded_value =', morsel.coded_value)
#     #     for name in morsel.keys():
#     #         if morsel[name]:
#     #             print('  {} = {}'.format(name, morsel[name]))

# #     for key, morsel in c.items():
# #         for name in morsel.keys():
# #             if morsel[name] :
# #                 return morsel.value, morsel[name]

# # def setCookie():
# #     c = cookies.SimpleCookie()
# #     # A cookie with a value that has to be encoded to fit into the header
# #     c['sessionId'] = ''.join(random.choice(string.ascii_lowercase) for i in range(4)) + str(random.randint(1,1000))+''.join(random.choice(string.ascii_lowercase) for i in range(3))
# #     # A cookie that expires  in 5 minutes
# #     # c['expires_at_time'] = 'cookie_value'
# #     time_to_live = datetime.timedelta(minutes=4)
# #     expires = (now + time_to_live)
# #     # Date format: Wdy, DD-Mon-YY HH:MM:SS GMT
# #     expires_at_time = expires.strftime('%a, %d %b %Y %H:%M:%S')
# #     c['sessionId']['expires'] = expires_at_time
# #     cookie,exp = show_cookie(c)
# #     return cookie ,exp

# # setCookie()    

# # def cookieExp(c):    
# #     fp = open("cookies.txt","r")
# #     for line in fp:
# #         if c in line:
# #             t = line.split("=")[1]
# #             # print(line)
# #             return t
# #         else:
# #             return False   

# # # fp = open("love.txt","r+")
# # # # for line in fp:
# # # def appendCookie(c,exp):
# # #     with open ("cookie.txt","a") as f:
# # #         f.write(c+"="+str(exp)+"\n")
# # #     f.close()

# # # def createCookie(c):
# # #     with open("cookie.txt", "r") as f:
# # #         lines = f.readlines()
# # #     f.close()
# # #     with open("cookie.txt", "w") as f:
# # #         for line in lines:
# # #             if str(c) in line:
# # #                 found = True
# # #                 t =strptime( line.split("=")[1])
                
# # #                 if t < now:
# # #                     f.write(line) 
# # #                     create = True
# # #                 else:
# # #                     create = False
# # #             else:
# # #                 found = False
# # #                 f.write(line)        
# # #     f.close()
# # #     if found:
# # #         return True if create else False
# # #     else:
# # #         return True
# # c=''
# # if c:
# #     print("fghj")
# import os , json , urllib.parse, uuid ,re,hashlib , random ,string
# from email.utils import formatdate
# from helper import *
# from datetime import *
# now = datetime.now()
# from http import cookies

# # def appendCookie(c,exp):
# #     with open ("cookie.txt","a") as f:
# #         f.write(c+"="+str(exp)+"\n")
# #     f.close()

# def createCookie(c):
#     with open("cookie.txt", "r") as f:
#         lines = f.readlines()
#     f.close()
#     found = False
#     with open("cookie.txt", "w") as f:
#         for line in lines:
#             if str(c) in line:
#                 found = True
#                 t = datetime.strptime(line.split("=")[-1].split("\n")[0],'%a, %d %b %Y %H:%M:%S')
#                 print("-->",t<now)
#                 if t < now:
                    
#                     create = True
#                 else:
#                     f.write(line) 
#                     create = False
#             else:
#                 found = False
#                 f.write(line)        
#     f.close()
#     if found:
#         return True if create else False
#     else:
#         return True

# print(createCookie("afmw248tkj"))

# # t = datetime.strptime( "13 Nov 2020 22:59:44",'%d %b %Y %H:%M:%S')
# # print(t<now)
'''Host: localhost:7000
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5 (Ergänzendes Update)) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Upgrade-Insecure-Requests: 1'''.encode("UTF-8").decode()
import sys
print(sys.argv[1])
print('hii')