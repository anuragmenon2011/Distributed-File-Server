import sys
import socket
import os
import configparser
import thread
#import time

def Main():
    host='localhost'
    backlog=50
    #print("In main")
    root_dir,pr=checkArgs()
    user_dict={}
    port=int(pr)
    config=configparser.ConfigParser(allow_no_value=True)
    config.optionxform=str
    try:
        config.read('dfs1.conf')       
    except:
        print("The conf file given does not exist.")
        sys.exit()

    user_list=config.options('Users')
    for y in user_list:
        name,passwd=y.split(' ')
        user_dict[name]=passwd
    
    #print(user_dict)
    #print(root_dir)
    #print(port)
    
    
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.bind((host,port))
    sock.listen(backlog)
    print("Listening for connections")

    while(True):
        #print("Waiting")
        cli_sock,addr=sock.accept()
        thread.start_new_thread(fork_command, (cli_sock,addr,user_dict,root_dir))
        
    cli_sock.close()
    
def fork_command(cli_sock,addr,user_dict,root_dir):
    valid_flag=False
    data=cli_sock.recv(1024)
    uname,passwd,user_comm=data.split('|||')
    if uname in user_dict.keys():
        #print("In first if")
        if user_dict[uname]==passwd:
            #print("In second if")
            cli_sock.send("Valid")
            valid_flag=True
        else:
            cli_sock.send('Invalid')
    if(valid_flag):
        #print("The user command is"+user_comm)
        if(user_comm=='PUT'):
            cwd=os.getcwd()
            dir_name=root_dir[1:]
            dir_serv=os.path.join(cwd,dir_name)
            if (not os.path.isdir(dir_serv)):
                print("The directory doesn't exists")
                os.makedirs(dir_name)
                #os.chdir(dir)
                #print(os.getcwd())
            #print(uname)
            usr_dir=os.path.join(dir_serv,uname)
            
            if (not os.path.isdir(usr_dir)):
                #print("User directory creating")
                os.makedirs(usr_dir)
            while(True):
                
                try:
                    #print("Waiting for fname")
                    fname=cli_sock.recv(1024)
                    #print(fname)
                    cli_sock.send("name_ACK")
                    if(fname=="CLOSE"):
                        #print("After closing")
                        cli_sock.close()
                        thread.exit()
                    else:    
                    #print(fname+"Thread start")
                        put_file(cli_sock,addr,root_dir,uname,fname)
                except socket.error:
                    #print("Closing after error")
                    cli_sock.close()
                    thread.exit()
                    
        if(user_comm=='GET'):
            
                fname=cli_sock.recv(1024)
                #print("Inside get"+fname)
                fl_list=[]
                cwd=os.getcwd()
                dir_name=root_dir[1:]
                serv_path=os.path.join(cwd,dir_name)
                user_path=os.path.join(serv_path,uname)
                #print(user_path)
                if (os.path.isdir(user_path)):
                    file_list=os.listdir(user_path)
                    #print(file_list)
                    for f in file_list:
                        l=f[1:]
                        z=l[:-2]
                        if(z==fname):
                            fl_list.append(f)
                    #print("The final list")
                    #print(fl_list)
                    if(len(fl_list)==0):
                        #print("NACK final list empty")
                        cli_sock.send("NACK")
                    else:
                        for files in fl_list:
                            get_file(files,cli_sock,user_path)
                        cli_sock.close()
                        thread.exit()    
                else:
                    #print("In else")
                    cli_sock.send("NACK")
                    
        if(user_comm=='LIST'):
            ready_ack=cli_sock.recv(1024)
            #print('ready ack'+ready_ack)
            if(ready_ack=='Ready'):
                cwd=os.getcwd()
                dir_name=root_dir[1:]
                serv_path=os.path.join(cwd,dir_name)
                user_path=os.path.join(serv_path,uname)
                #print(user_path)
                file_str=''
                if (os.path.isdir(user_path)):
                    file_list=os.listdir(user_path)
                    file_len=len(file_list)
                    i=0
                    for files in file_list:
                        if i==file_len-1:
                            file_str=file_str+files
                            break
                        file_str=file_str+files+'|||'
                        i=i+1
                    #print(file_str)
                    cli_sock.sendall(file_str)
                else:
                    #print("In else")
                    cli_sock.send("NACK")
def get_file(fname,cli_sock,user_path):
    #print("In get method")
    cli_sock.sendall("fname|||"+fname)
    fl_hn=open(os.path.join(user_path,fname),'rb')
    dat_ch=fl_hn.read()
    #for chunk in iter(lambda: fl_hn.read(1024), ''):
    cli_sock.sendall(dat_ch)  
    data_ack=cli_sock.recv(1024)
    #print(data_ack)  
    
        
def put_file(cli_sock,addr,root_dir,uname,fname):
    
    
    #print(fname)
    f1=open('.'+root_dir+'/'+uname+'/.'+fname,'wb')
    cli_sock.settimeout(2.0)
    
        #f2=open('.'+root_dir+'/'+uname+'/.'+fname)
    while(1):
        try:
            file_chunk=cli_sock.recv(1024)
            if(file_chunk):
            
            
                f1.write(file_chunk)

            
            else:
                #print("Closing file")
                f1.close()
            
                cli_sock.send("data_ACK")
            
                break
    
        except socket.timeout:
            #print("Closing file")
            f1.close()
            
            cli_sock.send("ACK")
            cli_sock.settimeout(None)
            break
        
                    
def checkArgs():
    if(len(sys.argv)!=4):
        print("Kindly provide the port number and the root directory for the server to listen")
        sys.exit()
    else:
        root_dir=sys.argv[1]
        port=sys.argv[2]
        #print(pr,tout)
        return root_dir,port


if __name__=="__main__":
    Main()