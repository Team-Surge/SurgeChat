#!/bin/python
#File: surgeChatServer.py
#Author: Nicholas Gingerella
#Dependencies: Twisted
import random
import string
from twisted.internet import reactor, protocol, endpoints
from twisted.internet.defer import Deferred
from twisted.protocols import basic
import json

#generate random string
def randomMsg(size = 10, chars = string.ascii_letters + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

class SurgeChatProtocol(basic.LineReceiver):
    #Protocols are like individual connections, thus, I can store
    #info about each individual connection (like a name) in this
    #class. (NOT ENTIRELY SURE ABOUT THIS ;P)
    state = 'REGISTER'
    clientName = ''
    serverChallengeToken = None


    #when a client makes a connection to the server, this runs
    def connectionMade(self):
        self.factory.client_count += 1
        print 'new client'
        print 'current client count:', self.factory.client_count


    #when a client closes the connection, or the connection is lost,
    #this runs
    def connectionLost(self, reason):
        self.factory.client_count -= 1
        if self.clientName in self.factory.connectedClients:
            del self.factory.connectedClients[self.clientName]
            print 'connection with',self.clientName,'has been lost!'
            print 'current client count:', self.factory.client_count


    #Whenever the server recieves data from any of the clients, this method
    #will run
    def lineReceived(self, line):
        #print self.factory.connectedClients
        if self.state == 'REGISTER':
            self.handle_REGISTER(line)
        elif self.state == 'IS_CLIENT':
            self.handle_CLIENT(line)
        elif self.state == 'CHALLENGE_SERVER':
            self.handle_CHALLENGE(line)
        elif self.state == 'IS_SERVER':
            self.handle_SERVER(line)
        else:
            print 'ERROR: UNKNOWN STATE!'


    def handle_REGISTER(self,line):
        inputMsg = json.loads(line)
        serverMsg = None
        clientMsg = None

        if self.isServerMessage(inputMsg):
            print 'This is the Server Message!'
            serverMsg = json.loads(line)
            print serverMsg
            
            #This is the initial connection message from the server
            #Now we need to challenge it to make sure it's the real
            #deal. We will send a random string with length of 128 chars
            self.serverChallengeToken = randomMsg(128) 
            challengeMsg = '{"challenge":"' + self.serverChallengeToken + '"}'
            self.sendLine(challengeMsg)
            self.state = 'CHALLENGE_SERVER'

        elif self.isClientMessage(inputMsg):
            print 'This is a Client Message!'
            clientMsg = json.loads(line)
            self.clientName = clientMsg["senderID"]
            print clientMsg 

            if self.clientName not in self.factory.connectedClients:
                self.addClient()
                self.state = 'IS_CLIENT'

            else:
                print self.clientName,'Client can only have 1 connection to server'
                self.transport.write('only 1 connection to chat server per user')

                #reset client name so we don't accidentally kick off the other
                #connection
                self.clientName = ''
                self.transport.loseConnection()
        else:
            print 'invalid request from client, closing client connection'
            self.transport.loseConnection()


    #The server has sent me a response to my challenge, I will now check its
    #returned encoded string to see if it matches my encoded string
    def handle_CHALLENGE(self, line):
        print 'in handle challenge state!'
        parsedResponse = json.loads(line)
        print parsedResponse['challengeResponse']
        encryptedChallenge = 'lol' #TODO: encrypt same way tom does
        if parsedResponse["challengeResponse"] == encryptedChallenge:
          print 'The response is correct!'
          self.sendLine('{"":""}')
          self.state = 'IS_SERVER'


    #TODO: implement server communication
    #THIS IS THE CORE OF THE CHAT SERVER!!!
    def handle_SERVER(self, line):
        inputMsg = json.loads(line)
        serverMsg = None
        
        #do nothing if the server doesn't verify
        if self.isServerMessage(inputMsg) == False:
            print 'server failed verification'
            return

        #if it is a proper server message, do stuff
        print 'server message recieved'
        serverMsg = inputMsg
        print serverMsg


    def handle_CLIENT(self,line):
        inputMsg = json.loads(line)
        clientMsg = None

        #verify that this is teh client and that the request isn't
        #malicious
        if self.verifyIsClient(inputMsg) == False:
            print 'bad request from client', self.clientName
            self.transport.write('ERROR: Improper Request\n')
            return

        clientMsg = json.loads(line)
        print 'Message received from',clientMsg["senderID"]
        print clientMsg 


    #TODO: implement server verify
    #Check that there is only 1 connection that is a server
    def verifyIsServer(self, jsonMsg):
        #is the message in the proper format for a client
        if self.isServerMessage(jsonMsg):
            print 'proper server message'
            return True
        
        #the previous criteria didn't pass
        return False


    #Is this a properly formatted client AND is the senderID match up
    #with the name of the current connection (is this an imposter?)
    def verifyIsClient(self, jsonMsg):
        #is the message in the proper format for a client
        if self.isClientMessage(jsonMsg):
            #does the senderID of the client message match the
            #client name given to the current client
            if jsonMsg["senderID"] == self.clientName:
                #the client should be in the connectedClients list
                if self.clientName in self.factory.connectedClients:
                    return True
        
        #the previous criteria didn't pass
        return False


    #add the name of the currently connected client to the connectedClients list
    def addClient(self):
        print 'adding',self.clientName,'to connected clients'
        self.factory.connectedClients[self.clientName] = self
        print 'connected clients:',
        for key in self.factory.connectedClients:
            print key,
        print ''

    
    #is the json message formatted appropriately for a client message?
    def isClientMessage(self,jsonMsg):
        if 'messageType' in jsonMsg:
            if jsonMsg['messageType'] != 'surgeclient':
                return False
            if 'senderID' in jsonMsg:
                if 'message' in jsonMsg:
                    return True
        return False


    #is the json message formatted appropriately for a server message?
    def isServerMessage(self,jsonMsg):
        if 'messageType' in jsonMsg:
            if jsonMsg['messageType'] != 'surgeserver':
                return False
            if 'serverToken' in jsonMsg:
              if 'conversationID' in jsonMsg:
                  if 'senderID' in jsonMsg:
                      if 'recipientID' in jsonMsg:
                            if 'message' in jsonMsg:
                                return True
        return False
            



#stores info about all connections
class surgeFactory(protocol.ServerFactory):
    protocol = SurgeChatProtocol
    surgeServerID = 'Surge1234' 
    client_count = 0
    connectedClients = {}
    openConversations = {}


#create server and start listening on port 8000
endpoints.serverFromString(reactor, 'tcp:8000').listen(surgeFactory())

#start the reactor!
reactor.run()
