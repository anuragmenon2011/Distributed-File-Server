Distributed File Server:

Client:

1. As soon as the client is run it loads the username and password from the config file and also the servers on which it wants to connect.
2. Them it prompts the user for the operation it would like to perform. Depending on the command given by the user, the control is forked to the respective method.
3. In any case the username and password is sent to each server at connection and authenticated against the username and password in server config file.
4. In case of put first the file is broken into almost 4 equal chunks. The MD% of the file is calculated and the modulus 4 of the md5 values determines which chunks	
   goes where. We maintain a deque and rotate it to get the chunk value to the server.
5. These values are stored as a key in a dictionary and the value will be the chunk value.
6. We connect to the servers one by one and send the filename fllowed by the value which should be written.
7. In case of get the filename is sent to the server and then the content is read in a temporary file. Then the file is combined and read int a single file.
8. In case of list the filename is sent to the servers and the filename is checked in the user directory. And then we create a dictionory to check if the file can be
   reconstructed.
9. Each server is set with a timeout of 2 seconds. And if the server doesn't respond it is considered to be down.


Server:

1. Each server listens to a port provided at command line. Then the first command received is the username,password and the user command. The username and password 
   are authenticated and the control is forked out to the respective command.
2. Each user should have his/her directory inside the folder intended for the particular server.
3. In case of put, the file is opened with the name sent by client and the content is written in it. The servers are connected in a round robin fashion.
4. In case of get, the file name is sent and the chunk file name is stripped and compared with the filename requested. If it matches the chunk files are sent 
   to the client to be reconstructed.
5. In case of list the filename is received, and all the matching files are sent as a single string with delimiters.

