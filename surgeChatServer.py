#!/bin/python
#File: surgeChatServer.py
#Author: Nicholas Gingerella
#Dependencies: Twisted

from twisted.internet import reactor, protocol, endpoints
from twisted.internet.defer import Deferred
from twisted.protocols import basic
import json

class SurgeChatProtocol(basic.LineReceiver):
    #Protocols are like individual connections, thus, I can store
    #info about each individual connection (like a name) in this
    #class. (NOT ENTIRELY SURE ABOUT THIS ;P)
    state = 'REGISTER'
    clientName = ''



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
        elif self.state == 'IS_SERVER':
            self.handle_SERVER(line)
        else:
            print 'ERROR: UNKNOWN STATE!'


    def handle_REGISTER(self,line):
        inputMsg = json.loads(line)
        serverMsg = None
        clientMsg = None

        if self.isServerMessage(inputMsg):
            print 'This is a Server Message!'
            serverMsg = json.loads(line)
            print serverMsg 
            self.clientName = 'SERVER-ID'
            self.state = 'IS_SERVER'

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


    #TODO: implement server communication
    #THIS IS THE CORE OF THE CHAT SERVER!!!
    def handle_SERVER(self, line):
        inputMsg = json.loads(line)
        serverMsg = None
        
        #do nothing if the server doesn't verify
        if self.verifyIsServer(inputMsg) == False:
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
            if 'conversationID' in jsonMsg:
                if 'senderID' in jsonMsg:
                    if 'recipientID' in jsonMsg:
                        if jsonMsg['senderID'] != jsonMsg['recipientID']:
                            if 'message' in jsonMsg:
                                return True
        return False
            



#stores info about all connections
class surgeFactory(protocol.ServerFactory):
    protocol = SurgeChatProtocol
    client_count = 0
    connectedClients = {}
    openConversations = {}


#create server and start listening on port 8000
endpoints.serverFromString(reactor, 'tcp:8000').listen(surgeFactory())

#start the reactor!
reactor.run()
