import server ,os
from threading import *
from config import *

def action(todo,Port):
    if todo.upper()=="START": 
        server.startserver(Port)        
    elif todo.upper()=="STOP":
        try:
            server.stopserver()
        except:
            pass
        print(" Server stopped! \n")        
        os._exit(1)
        
last=0
while True:
    user_input = input("Type start or stop the server (or exit to end main): \n")
    try:
        if user_input.upper()=="START" and last == 0:
            last = 1
            Port = int(input('Port :'))
            if Port < 2048:
                print("Invalid Port\n")
                continue  
            t1 = Thread(target=action, args=(user_input,Port))
            t1.start()    
        if user_input.upper()== 'STOP' and last == 1:
            Port=PORT
            last =0
            t1 = Thread(target=action, args=(user_input,Port))
            t1.start()
        if user_input.upper() == 'EXIT':
            break        
    except:
        print("Error !!\n")
        os._exit(1)