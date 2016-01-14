import configparser
import sys
import os
import hashlib
import collections
import socket
#import time


def Main():
    conf_file=checkArgs()
    config=configparser.ConfigParser(delimiters=(' '))
    try:
        config.read(conf_file)       
    except:
        print("The conf file given does not exist.")
        sys.exit()
    try:
        server1=config.get('Servers','Server:DFS1')
        server2=config.get('Servers','Server:DFS2')
        server3=config.get('Servers','Server:DFS3')
        server4=config.get('Servers','Server:DFS4')
    except:
        print("Check your conf file for details. Some details are missing")
        sys.exit()        
    addr1,port1=server1.split(':')
    
    addr2,port2=server2.split(':')
    addr3,port3=server3.split(':')
    addr4,port4=server4.split(':')
    try:
        uname=config.get('User','Username')
        passwd=config.get('User','Password')
    except:
        print("Check your conf file for details. Some details are missing")
        sys.exit()
    conf_tuple=(addr1,port1,addr2,port2,addr3,port3,addr4,port4,uname,passwd)
    user_command=raw_input("Enter the operation you would like to perform. GET,PUT or LIST: ")
    comm_list=user_command.split()
    #print(comm_list)
    if(len(comm_list)==1 and comm_list[0]!='LIST'):
        
        #print("Invalid Command1")
        sys.exit()
    if(len(comm_list)==2 and (comm_list[0] not in ['GET','PUT'])):
        #print("Invalid Command2")
        sys.exit()
    if(len(comm_list)>2):
        #print("Invalid Command3")
        sys.exit()
    
    if comm_list[0]=='PUT':
        filename=comm_list[1]
        put_to_server(filename,conf_tuple)
    if comm_list[0]== 'GET':
        filename=comm_list[1]
        get_from_server(filename,conf_tuple) 
    if comm_list[0] == 'LIST':
        list_files(conf_tuple)
        
def list_files(conf_tuple):
    list_dict={}
    #print("In List method")
    addr1=conf_tuple[0]
    port1=int(conf_tuple[1])
    addr2=conf_tuple[2]
    port2=int(conf_tuple[3])
    addr3=conf_tuple[4]
    port3=int(conf_tuple[5])
    addr4=conf_tuple[6]
    port4=int(conf_tuple[7])
    uname=conf_tuple[8]
    passwd=conf_tuple[9]
    #Connecting to first server
    f1=False
    sock1=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock1.settimeout(1.0)
    try:
        sock1.connect((addr1,port1))
        sock1.send(uname+'|||'+passwd+'|||LIST')
        f1=True
    except:
        print("Couldn't create socket with first server")
    if(f1==True):
        try:
            data=sock1.recv(1024)
        except socket.timeout:
            print("Socket not responding")
            sock1.settimeout(None)
        if(data):
            #print(data)
            if(data=='Invalid'):
                print("The user crediantials are invalid. Kindly check your credentials")
                #sys.exit()
            if(data=='Valid'):
                sock1.send('Ready')
                data1=sock1.recv(1024)
                #print(data1)
                if(data1=='NACK'):
                    print("No directory for user found.")
                    sys.exit()
            
                else:
                    lo_list=data1.split('|||')
                    for x in lo_list:
                        chunk=x[-1]
                        fn=x[1:]
                        #print(fn)
                        f_name=fn[:-2]
                        if f_name in list_dict:
                            
                            list_dict[f_name]=list_dict[f_name]+'|||'+chunk
                        else:
                            list_dict[f_name]=chunk
                        #print("Chunk number"+chunk+"Name"+f_name)
                        #print(list_dict)
    #Connecting second server
    f1=False
    sock2=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock2.settimeout(2.0)
    try:
        sock2.connect((addr2,port2))
        sock2.send(uname+'|||'+passwd+'|||LIST')
        f1=True
    except:
        print("Couldn't connect to second server")
    if(f1==True):    
        #sock2.send(uname+'|||'+passwd+'|||LIST')
        try:
            data=sock2.recv(1024)
            #print(data)
        except socket.timeout:
            print("Socket timedout. Server refused connection ")
            sock2.settimeout(None)
        if(data):
            if(data=='Invalid'):
                print("The user crediantials are invalid. Kindly check your credentials")
                #sys.exit()
            if(data=='Valid'):
                sock2.send('Ready')
                data1=sock2.recv(1024)
                #print(data1)
                if(data1=='NACK'):
                    print("No directory for user found.")
                    sys.exit()
            
                else:
                    lo_list1=data1.split('|||')
                    for x in lo_list1:
                        chunk=x[-1]
                        fn=x[1:]
                        #print(fn)
                        f_name=fn[:-2]
                        if f_name in list_dict:
                            list_dict[f_name]=list_dict[f_name]+'|||'+chunk
                        else:
                            list_dict[f_name]=chunk
                        #print("Chunk number"+chunk+"Name"+f_name)
                        #print(list_dict)
                
    #Connecting to third server
    f1=False
    sock3=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock3.settimeout(2.0)
    try:
        sock3.connect((addr3,port3))
        sock3.send(uname+'|||'+passwd+'|||LIST')
        f1=True
    except:
        print("Couldn't connect to third server")
        
    
    if(f1==True):
        try:
            data=sock3.recv(1024)
            #print(data)
        except socket.timeout:
            print("The socket connection was refused by the server3.")
            sock3.settimeout(None)
        if(data):
            if(data=='Invalid'):
                print("The user crediantials are invalid. Kindly check your credentials")
                #sys.exit()
            if(data=='Valid'):
                sock3.send('Ready')
                data1=sock3.recv(1024)
                #print(data1)
                if(data1=='NACK'):
                    print("No directory for user found.")
                    sys.exit()
            
                else:
                    lo_list2=data1.split('|||')
                    for x in lo_list2:
                        chunk=x[-1]
                        fn=x[1:]
                        #print(fn)
                        f_name=fn[:-2]
                        if f_name in list_dict:
                            list_dict[f_name]=list_dict[f_name]+'|||'+chunk
                        else:
                            list_dict[f_name]=chunk
                        #print("Chunk number"+chunk+"Name"+f_name)
                        #print(list_dict)
                        
    #Connecting to fourth server
    f1=False
    sock4=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock4.settimeout(2.0)
    try:
        sock4.connect((addr4,port4))
        sock4.send(uname+'|||'+passwd+'|||LIST')
        f1=True
    except:
        print("Couldn't connect to 4th server")
        
    if(f1==True):
        try:
            data=sock4.recv(1024)
            #print(data)
        except:
            print("Socket connection was refused")
            sock4.settimeout(None)
        if(data=='Invalid'):
            print("The user crediantials are invalid. Kindly check your credentials")
            #sys.exit()
        if(data=='Valid'):
            sock4.send('Ready')
            data1=sock4.recv(1024)
            #print(data1)
            if(data1=='NACK'):
                print("No directory for user found.")
                sys.exit()
        
            else:
                lo_list3=data1.split('|||')
                for x in lo_list3:
                    chunk=x[-1]
                    fn=x[1:]
                    #print(fn)
                    f_name=fn[:-2]
                    if f_name in list_dict:
                        list_dict[f_name]=list_dict[f_name]+'|||'+chunk
                    else:
                        list_dict[f_name]=chunk
                    #print("Chunk number"+chunk+"Name"+f_name)
                    #print(list_dict)
     
                
    for key in list_dict:
        i1=0
        i2=0
        i3=0
        i4=0
        o_list=list_dict[key]
        temp_list=o_list.split('|||')
        #print(temp_list)
        for i in temp_list:
            if i=='1':
                i1=i1+1
            elif i=='2':
                i2=i2+1
            elif i=='3':
                i3=i3+1
            elif i=='4':
                i4=i4+1
        if(i1>0 and i2>0 and i3>0 and i4>0):
            print(key)
        else:
            print(key+'    [incomplete]')
    
    
            
def get_from_server(filename,conf_tuple):
    #print("In Get method")
    addr1=conf_tuple[0]
    port1=int(conf_tuple[1])
    addr2=conf_tuple[2]
    port2=int(conf_tuple[3])
    addr3=conf_tuple[4]
    port3=int(conf_tuple[5])
    addr4=conf_tuple[6]
    port4=int(conf_tuple[7])
    uname=conf_tuple[8]
    passwd=conf_tuple[9]
    #Connecting to first server
    f1=False
    sock1=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock1.settimeout(2.0)
    try:
        sock1.connect((addr1,port1))
        sock1.send(uname+'|||'+passwd+'|||GET')
        f1=True
    except:
        ("Connection couodn't be made with first server")
    if(f1==True):
        try:
            data=sock1.recv(1024)
            #print(data)
        except socket.timeout:
            print("Connection refused by first server")
            sock1.settimeout(None)
        if(data):    
            if(data=='Invalid'):
                print("The user crediantials are invalid. Kindly check your credentials")
                #sys.exit()
            if(data=='Valid'):
                sock1.send(filename)
                #sock1.settimeout(2.0)
                flee=1
                floo=1
                msg1=''
                while flee==1:
                    
                    data1=sock1.recv(1024)
                    #print(data1)
                    if(data1=='NACK'):
                        print("No file found on server 1")
                        break
                    else:
                        
                        if(data1):
                            if(data1.split('|||')[0]=='fname'):
                                fname=data1.split('|||')[1]
                                while floo==1:
                                    #print("Inside floo")
                                    sock1.settimeout(2.0)
                                    try:
                                        data2=sock1.recv(1024)
                                        msg1=msg1+data2
                                    except:
                                        fl=open(fname,'wb')
                                        fl.write(msg1)
                                        floo=0
                                        fl.close()
                                        sock1.settimeout(None)   
                                        sock1.send("ACK")
                        
                        flee=0
                        #print("File written")
                        floo=1
                        flee=1
                        msg1=''
                        while flee==1:
                            
                            data3=sock1.recv(1024)
                            #print(data3)
                            if(data3):
                                if(data3.split('|||')[0]=='fname'):
                                    fname=data3.split('|||')[1]
                                    while floo==1:
                                        #print("Inside floo")
                                        sock1.settimeout(2.0)
                                        try:
                                            data4=sock1.recv(1024)
                                            msg1=msg1+data4
                                        except:
                                            fl=open(fname,'wb')
                                            fl.write(msg1)
                                            sock1.settimeout(None)
                                            floo=0   
                                            fl.close()
                                            sock1.send("ACK")
                            
                            flee=0
                        #print("File written")  
        
        
        
        
    #Connecting to second server
    f1=False
    sock2=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock2.settimeout(2.0)
    try:
        sock2.connect((addr2,port2))
        sock2.send(uname+'|||'+passwd+'|||GET')
        f1=True
    except:
        print("Couldn't connect to second server")
    if(f1==True):
        try:
            data=sock2.recv(1024)
            #print(data)
        except socket.timeout:
            print("Connection refused by second server")
            sock2.settimeout(None)
        if(data):
            if(data=='Invalid'):
                print("The user crediantials are invalid. Kindly check your credentials")
                #sys.exit()
            if(data=='Valid'):
                sock2.send(filename)
                #sock1.settimeout(2.0)
                flee=1
                floo=1
                msg1=''
                while flee==1:
                    
                    data5=sock2.recv(1024)
                    #print(data5)
                    if(data5=='NACK'):
                        print("No file found on server2")
                        break
                    else:
                        if(data5):
                            if(data5.split('|||')[0]=='fname'):
                                fname=data5.split('|||')[1]
                                while floo==1:
                                    #print("Inside floo")
                                    sock2.settimeout(2.0)
                                    try:
                                        data6=sock2.recv(1024)
                                        msg1=msg1+data6
                                    except:
                                        fl=open(fname,'wb')
                                        fl.write(msg1)
                                        fl.close()
                                        sock2.settimeout(None)
                                        floo=0   
                                        sock2.send("ACK")
                        
                        flee=0
                        #print("File written")
                        floo=1
                        flee=1
                        msg1=''
                        while flee==1:
                            
                            data7=sock2.recv(1024)
                            #print(data7)
                            if(data7):
                                if(data7.split('|||')[0]=='fname'):
                                    fname=data7.split('|||')[1]
                                    while floo==1:
                                        #print("Inside floo")
                                        sock2.settimeout(2.0)
                                        try:
                                            data8=sock2.recv(1024)
                                            msg1=msg1+data8
                                        except:
                                            fl=open(fname,'wb')
                                            fl.write(msg1)
                                            sock2.settimeout(None)
                                            floo=0   
                                            fl.close()
                                            sock2.send("ACK")
                            
                            flee=0
                        #print("File written")
    
    
    #Connecting to third server
    f1=False
    sock3=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock3.settimeout(2.0)
    try:
        sock3.connect((addr3,port3))
        sock3.send(uname+'|||'+passwd+'|||GET')
        f1=True
    except:
        print("Couldn't connect to third server")
    if(f1==True):
        try:
            data=sock3.recv(1024)
            #print(data)
        except socket.timeout:
            print("Socket connection refused.")
            sock3.settimeout(None)
        if(data):
            if(data=='Invalid'):
                print("The user crediantials are invalid. Kindly check your credentials")
                #sys.exit()
            if(data=='Valid'):
                sock3.send(filename)
                
                #sock1.settimeout(2.0)
                flee=1
                floo=1
                msg1=''
                while flee==1:
                    
                    data9=sock3.recv(1024)
                    if(data9=='NACK'):
                        print("No file found on server3")
                        break
                    #print(data9)
                    else:
                        if(data9):
                            if(data9.split('|||')[0]=='fname'):
                                fname=data9.split('|||')[1]
                                while floo==1:
                                    #print("Inside floo")
                                    sock3.settimeout(2.0)
                                    try:
                                        data10=sock3.recv(1024)
                                        msg1=msg1+data10
                                    except:
                                        fl=open(fname,'wb')
                                        fl.write(msg1)
                                        sock3.settimeout(None)
                                        floo=0   
                                        fl.close()
                                        sock3.send("ACK")
                        
                        flee=0
                        #print("File written")
                        floo=1
                        flee=1
                        msg1=''
                        while flee==1:
                            
                            data11=sock3.recv(1024)
                            #print(data11)
                            if(data11):
                                if(data11.split('|||')[0]=='fname'):
                                    fname=data11.split('|||')[1]
                                    while floo==1:
                                        #print("Inside floo")
                                        sock3.settimeout(2.0)
                                        try:
                                            data12=sock3.recv(1024)
                                            msg1=msg1+data12
                                        except:
                                            fl=open(fname,'wb')
                                            fl.write(msg1)
                                            sock3.settimeout(None)
                                            floo=0   
                                            fl.close()
                                            sock3.send("ACK")
                            
                            flee=0
                        #print("File written")
    
    #Connecting to fourth server
    f1=False
    sock4=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock4.settimeout(2.0)
    try:
        sock4.connect((addr4,port4))
        sock4.send(uname+'|||'+passwd+'|||GET')
        f1=True
    except:
        print("Couldn't connect to fourth server")
    if(f1==True):
        try:    
            data=sock4.recv(1024)
            #print(data)
        except socket.timeout:
            print("Socket connection refused")
            sock4.settimeout(None)
        if(data):
            if(data=='Invalid'):
                print("The user crediantials are invalid. Kindly check your credentials")
                #sys.exit()
            if(data=='Valid'):
                sock4.send(filename)
                
                #sock1.settimeout(2.0)
                flee=1
                floo=1
                msg1=''
                while flee==1:
                    
                    data13=sock4.recv(1024)
                    #print(data13)
                    if(data13=='NACK'):
                        print("No files found on server 4")
                        break
                    else:
                        if(data13):
                            if(data13.split('|||')[0]=='fname'):
                                fname=data13.split('|||')[1]
                                while floo==1:
                                    #print("Inside floo")
                                    sock4.settimeout(2.0)
                                    try:
                                        data14=sock4.recv(1024)
                                        msg1=msg1+data14
                                    except:
                                        fl=open(fname,'wb')
                                        fl.write(msg1)
                                        sock4.settimeout(None)
                                        floo=0   
                                        fl.close()
                                        sock4.send("ACK")
                        
                        flee=0
                        #print("File written")
                        floo=1
                        flee=1
                        msg1=''
                        while flee==1:
                            
                            data15=sock4.recv(1024)
                            #print(data15)
                            if(data15):
                                if(data15.split('|||')[0]=='fname'):
                                    fname=data15.split('|||')[1]
                                    while floo==1:
                                        #print("Inside floo")
                                        sock4.settimeout(2.0)
                                        try:
                                            data16=sock4.recv(1024)
                                            msg1=msg1+data16
                                        except:
                                            fl=open(fname,'wb')
                                            fl.write(msg1)
                                            sock4.settimeout(None)
                                            floo=0   
                                            fl.close()
                                            sock4.send("ACK")
                            
                            flee=0
                        #print("File written")
    
    if(os.path.isfile('.'+filename+'.1') and os.path.isfile('.'+filename+'.2') and os.path.isfile('.'+filename+'.3') and os.path.isfile('.'+filename+'.4')):
        print("Writng the main file")
        ft1=open('.'+filename+'.1','rb')
        ft2=open('.'+filename+'.2','rb')
        ft3=open('.'+filename+'.3','rb')
        ft4=open('.'+filename+'.4','rb')
        ftt1=ft1.read()
        ftt2=ft2.read()
        ftt3=ft3.read()
        ftt4=ft4.read()
        fg=open(filename,'wb')
        fg.write(ftt1+ftt2+ftt3+ftt4)
        fg.close()
        ft1.close()
        ft2.close()
        ft3.close()
        ft4.close()
        os.remove('.'+filename+'.1')
        os.remove('.'+filename+'.2')
        os.remove('.'+filename+'.3')
        os.remove('.'+filename+'.4')
    else:
        print(filename + ':[incomplete] Cannot be constructed')
        
        
        
           
def put_to_server(filename,conf_tuple):
    #print("In put method")
    #print(filename)
    numchunk=4
    addr1=conf_tuple[0]
    port1=int(conf_tuple[1])
    addr2=conf_tuple[2]
    port2=int(conf_tuple[3])
    addr3=conf_tuple[4]
    port3=int(conf_tuple[5])
    addr4=conf_tuple[6]
    port4=int(conf_tuple[7])
    uname=conf_tuple[8]
    passwd=conf_tuple[9]
    #print(uname,passwd,addr1,port1)
    try:
        fl=open(filename,'rb')
    except:
        print("The file doesn't exist. Kindly check the directory")
        sys.exit()
    file_size=os.path.getsize(filename)
    chunk_size=int(float(file_size)/float(numchunk))
    total_bytes=0
    #print(file_size)
    #print(chunk_size)
    file_map={}
    for x in range(numchunk):
        
        if x==numchunk-1:
            chunks_size=file_size-total_bytes
        
        data=fl.read(chunk_size)
        total_bytes+=len(data)
        file_map[x+1]=data
    md5_data=fl.read()
    md5sum=hashlib.md5(md5_data).hexdigest() 
    md5_num=int(md5sum,16)
    loc_pnt=md5_num%4
    print("hash value"+str(loc_pnt))  
    rot_list=collections.deque([(1,2),(2,3),(3,4),(4,1)])
    rot_list.rotate(loc_pnt)
    #print(rot_list)
    
    #Connecting to first Server 
    f1=False
    sock1=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock1.settimeout(2.0)
    try:
        sock1.connect((addr1,port1))
        sock1.send(uname+'|||'+passwd+'|||PUT')
        f1=True
    except:
        print("Couldn't connect to first server")
    if(f1==True):
        try:
            sock1.settimeout(None)
            data=sock1.recv(1024)
            #print(data)
        except socket.timeout:
            print("Socket connection timedout")
            sock1.settimeout(None)
        if(data):
            if(data=='Invalid'):
                print("The user crediantials are invalid. Kindly check your credentials")
                #sys.exit()
            if(data=='Valid'):
                fl_name=filename+'.'+str(rot_list[0][0])
                sock1.send(fl_name)
                name_ack=sock1.recv(1024)
                #print("This is name ack"+name_ack)
                if(name_ack=="name_ACK"):
                    sock1.send(file_map[rot_list[0][0]])
                    data_ack=sock1.recv(1024)
                    #print(data_ack)
                
                
                
                fl_name=filename+'.'+str(rot_list[0][1])
                sock1.send(fl_name)
                name_ack1=sock1.recv(1024)
                #print("This is name_ack1"+name_ack1)
                if(name_ack1=="name_ACK"):
                    sock1.send(file_map[rot_list[0][1]])
                    ack=sock1.recv(1024)
                    #print(ack)
                    #print("Sent")
                
                sock1.send("CLOSE")
        
    #Connecting to second server
    f1=False
    sock2=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock2.settimeout(2.0)
    try:
        sock2.connect((addr2,port2))
        sock2.send(uname+'|||'+passwd+'|||PUT')
        f1=True
    except:
        print("Couldn't connect to  second server")
    if(f1==True):
        try:
            sock2.settimeout(None)
            data=sock2.recv(1024)
            #print(data)
        except socket.timeout:
            print("Socket connection timedout")
            sock2.settimeout(None)
        if(data):
            if(data=='Invalid'):
                print("The user crediantials are invalid. Kindly check your credentials")
                #sys.exit()
            if(data=='Valid'):
                fl_name=filename+'.'+str(rot_list[1][0])
                sock2.send(fl_name)
                name_ack=sock2.recv(1024)
                
                if(name_ack=="name_ACK"):
                    sock2.send(file_map[rot_list[1][0]])
                    data_ack=sock2.recv(1024)
                    #print(data_ack)
                
                
                
                fl_name=filename+'.'+str(rot_list[1][1])
                sock2.send(fl_name)
                name_ack1=sock2.recv(1024)
                
                if(name_ack1=="name_ACK"):
                    sock2.send(file_map[rot_list[1][1]])
                    ack=sock2.recv(1024)
                    #print(ack)
                    #print("Sent")
                sock2.send("CLOSE")   
    #Connecting to third server  
    f1=False
    sock3=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock3.settimeout(2.0)
    try:
        sock3.connect((addr3,port3))
        sock3.send(uname+'|||'+passwd+'|||PUT')
        f1=True
    except:
        print("Couldn't connect to third server")
    if(f1==True):
        try:    
            sock3.settimeout(None)
            data=sock3.recv(1024)
            #print(data)
        except socket.timeout:
            print("Socket connection timedout")
            sock3.settimeout(None)
        if(data):
            if(data=='Invalid'):
                print("The user crediantials are invalid. Kindly check your credentials")
                #sys.exit()
            if(data=='Valid'):
                fl_name=filename+'.'+str(rot_list[2][0])
                sock3.send(fl_name)
                name_ack=sock3.recv(1024)
                
                if(name_ack=="name_ACK"):
                    sock3.send(file_map[rot_list[2][0]])
                    data_ack=sock3.recv(1024)
                    #print(data_ack)
                
                
                
                fl_name=filename+'.'+str(rot_list[2][1])
                sock3.send(fl_name)
                name_ack1=sock3.recv(1024)
                
                if(name_ack1=="name_ACK"):
                    sock3.send(file_map[rot_list[2][1]])
                    ack=sock3.recv(1024)
                    #print(ack)
                    #print("Sent")
                sock3.send("CLOSE")
    #Connecting to 4th server
    f1=False
    sock4=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock4.settimeout(2.0)
    try:
        sock4.connect((addr4,port4))
        sock4.send(uname+'|||'+passwd+'|||PUT')
        f1=True
    except:
        print("Couldn't connect to fourth server")
    if(f1==True):
        try:
            sock4.settimeout(None)
            data=sock4.recv(1024)
            #print(data)
        except:
            print("Socket connection timedout")
            sock4.settimeout(None)
        if(data):
            if(data=='Invalid'):
                print("The user crediantials are invalid. Kindly check your credentials")
                #sys.exit()
            if(data=='Valid'):
                fl_name=filename+'.'+str(rot_list[3][0])
                sock4.send(fl_name)
                name_ack=sock4.recv(1024)
                
                if(name_ack=="name_ACK"):
                    sock4.send(file_map[rot_list[3][0]])
                    data_ack=sock4.recv(1024)
                    #print(data_ack)
                
                
                
                fl_name=filename+'.'+str(rot_list[3][1])
                sock4.send(fl_name)
                name_ack1=sock4.recv(1024)
                
                if(name_ack1=="name_ACK"):
                    sock4.send(file_map[rot_list[3][1]])
                    ack=sock4.recv(1024)
                    #print(ack)
                    #print("Sent")
                sock4.send("CLOSE")    
def checkArgs():
    if(len(sys.argv)!= 2):
        print("The program requires 1 argument to run:The conf filename.Kindly provide the filename")
        sys.exit()
    else:
        conf_file=sys.argv[1]
        return conf_file
    
          
if __name__=="__main__":
    Main()