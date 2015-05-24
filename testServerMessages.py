#practice using python socket programming
import socket   #for socket
import os
import errno
import sys  #for exit
import time

#create TCP socket (AF_INET, STREAM socket)
#socket.socket returns a socket descriptor which can be used
#in other socket related functions.
#socket.socket(address family, socket type)
#AF_INET -> IP version 4 (IPv4)
#SOCK_STREAM -> socket uses connection oriented TCP protocol
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#if socket creation fails, python throws and exception called socket.error
#which must be caught
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except OSError as e:
    print("ERROR:",e)
    #print("Failed to create socket. Error code:", str(msg[0]), " , Error message:",msg[1])
    sys.exit()

print("Socket Created")

host = "127.0.0.1"
port = 8000

try:
    remote_ip = socket.gethostbyname(host)
except OSError as e:
    print("ERROR:",e)
    sys.exit()

print("IP address of", host, "is",  remote_ip)

#connect to remote server at "host" using port "port"
s.connect((host, port))

print("Socket Connected to", host, "on IP", remote_ip, "using port", port)

#in Python3, there is a different between "byte strings" and "unicode strings".
#strings surrounded by double quotes are unicode strings.
#send and sendall requires you to use byte strings. You can either define the string
#as a byte string by doing this:
#
#   message = b"GET / HTTP/1.1\r\n\r\n"
#             ^
#         prepend with b to make a byte string
#                  
#or you can use the "encode()" method to convert the regular unicode sting to a byte string
#and when recieving data and you want to convert it to a unicode string, use the decode() method
#   
#   s.sendall(message.encode()) <---- convert message into a byte string when used in socket sendall()
#   newmsg = s.recv(512).decode() <------ converts the byte string recieved from the socket into a unicode string
state = "connectRequest"
while True:
  time.sleep(1)
  if state == "connectRequest":
    message = '{"clientType":"surgeserver", "messageType":"connectRequest"}'
    try:
      s.sendall(message.encode())
    except (OSError,TypeError) as e:
      pass
      #print("ERROR:",e)
      #print("Send Failed")
    state = "challengeResponse"
  elif state == "challengeResponse":
    message = '{"clientType":"surgeserver", "messageType":"challengeResponse", "responseToken":"", "responseIV":"1111111111111111"}'
    try:
      s.sendall(message.encode())
    except (OSError,TypeError) as e:
      print("ERROR:",e)
      print("Send Failed")
    state = "connected"
  elif state == "connected":
    cv = input ("enter conversation ID:")
    u1 = input ("enter senderID:")
    u2 = input ("enter recipientID:")
    msg = input("msg from "+u1+" to "+u2+":")
    msg.replace('"','\"')
    message = '{"clientType":"surgeserver", "messageType":"chat", "conversationID":"'+cv+'", "senderID":"'+u1+'", "recipientID":"'+u2+'", "message":"'+msg+'"}'
    try:
      s.sendall(message.encode())
    except (OSError,TypeError) as e:
      print("ERROR:",e)
      print("Send Failed")

  #Now recieve data
  #4096 is the buffer size for the byte string we will recieve
  #also note that I'm decoding the data recieved, since we recieve it
  #as a byte string, and not a unicode string
  #reply = s.recv(4096)
  #print(reply.decode())

s.close()
