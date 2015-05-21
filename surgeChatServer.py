#!/bin/python
#File: surgeChatServer.py
#Author: Nicholas Gingerella
#Dependencies: Twisted
from surgeUtilities import randomMsg, enum
from twisted.internet import reactor, protocol, endpoints
from twisted.internet.defer import Deferred
from twisted.protocols import basic
import json

class SurgeChatProtocol(basic.LineReceiver):
    #Protocols are like individual connections, thus, I can store
    #info about each individual connection (like a name) in this
    #class.
    state = None
    clientType = None
    clientName = ''
    serverChallengeToken = None
    #when a client makes a connection to the server, this runs
    def connectionMade(self):
        print 'new client connected'
        self.factory.client_count += 1
        #initialize state and enumerators neede to maintain state
        self.states = self.factory.states #list of states is in the factory, but doing this to type less later on
        self.clientTypes = self.factory.clientTypes
        self.state = self.states.REGISTER


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
        if self.state == self.states.REGISTER:
            self.handle_REGISTER(line)
        elif self.state == self.states.IS_CLIENT:
            self.handle_CLIENT(line)
        elif self.state == self.states.CHALLENGE_SERVER:
            self.handle_CHALLENGE(line)
        elif self.state == self.states.IS_SERVER:
            self.handle_SERVER(line)
        else:
            print 'ERROR: UNKNOWN STATE!'
            self.transport.loseConnection()


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
            self.state = self.states.CHALLENGE_SERVER

        elif self.isClientMessage(inputMsg):
            print 'This is a Client Message!'
            clientMsg = json.loads(line)
            self.clientName = clientMsg["senderID"]
            print clientMsg 

            #check if current connections userID already exists in the connected
            #client dictionary, if so, this is a client is either an imposter or
            #is trying to log in to chat from 2 different phones, which is not allowed.
            #deny this connection
            if self.clientName not in self.factory.connectedClients:
                self.addClient()
                self.state = self.states.IS_CLIENT

            else:
                print self.clientName,'is already connected to chat server'
                self.sendLine('only 1 connection to chat server per user')

                #reset client name so we don't accidentally kick off the other
                #connection
                self.clientName = ''

                #close this connection
                self.transport.loseConnection()

        else:
            #this message was not formatted properly for either a normal client, nor the surge server
            print 'invalid request from client, closing client connection'
            self.transport.loseConnection()


    ################################################################################################
    #TODO: Implement AES encryption for initial authentication between Surge Server and Chat Server
    #      Details in the chat outline document
    ################################################################################################
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
          self.state = self.states.IS_SERVER


    ##########################################
    #TODO: Implement server communication
    #      THIS IS THE CORE OF THE CHAT SERVER!!!
    ##########################################
    #when the server sends a valid message containing information about a message, such as the
    #conversationID, senderID, recipientID, and message, I need to send the message to the 
    #recipient in the context of the correct conversation. Of course, I need to make sure the
    #recipient is connected to the chat server before I can send it, and if they are not connected,
    #throw the message away, they'll retrieve it when the log into chat later on, since it is stored
    #in the database
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


    #At the moment, we won't expect too much info coming from individual clients. We need this
    #to primarily handle the initial connection with the client, to make sure they get placed into
    #the connected clients dictionary if they are logged into chat
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


    #TODO: implement server verify (MIGHT NOT BE NEEDED AFTER AUTHENTICATION IS IMPLEMENTED)
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
        #the message must have the proper format for a client message
        if not self.isClientMessage(jsonMsg):
            return False

        #the senderID must match the client name associated with this
        #particular connection (to avoid users trying to imitate other users)
        if jsonMsg["senderID"] != self.clientName:
            return False

        #the client should already exist in the connected clients list
        #(how else would you get to this point?)
        if self.clientName not in self.factory.connectedClients:
            return False 
        
        #The client passed through all of the checkpoints, in which case,
        #it meets all of the criteria for a valid client message
        return True 


    #add the name of the currently connected client to the connectedClients list
    def addClient(self):
        print 'adding',self.clientName,'to connected clients'

        #add this client's protocol object to the dictionary, where the key is the
        #id of the client and the value is the protcol object. The protocol object
        #is needed in order to send data to the specific clients
        self.factory.connectedClients[self.clientName] = self

        #print the ids of the currently connect clients
        print 'connected clients:',
        for key in self.factory.connectedClients:
            print key,
        print ''


    #TODO: add "clientType" field 
    # is the json message formatted appropriately for a client message
    def isClientMessage(self,jsonMsg):
        if 'clientType' not in jsonMsg:
            return False

        if jsonMsg["clientType"] != 'surgeclient':
            return False

        if 'messageType' not in jsonMsg:
            return False

        if 'senderID' not in jsonMsg:
            return False

        if 'message' not in jsonMsg:
            return False

        # all the previous conditions didn't hold, so we have
        # a valid client message
        return True


    #TODO: add "serverType" field
    #is the json message formatted appropriately for a server message?
    def isServerMessage(self,jsonMsg):
        if 'clientType' not in jsonMsg:
            return False
        
        if jsonMsg["clientType"] != 'surgeserver':
            return False

        if 'messageType' not in jsonMsg:
            return False

        if 'serverToken' not in jsonMsg:
            return False

        if 'conversationID' not in jsonMsg:
            return False

        if 'senderID' not in jsonMsg:
            return False
        
        if 'recipientID' not in jsonMsg:
            return False

        if 'message' not in jsonMsg:
            return False
        
        # all the previous conditions didn't hold, so we have
        # a valid server message
        return True


#stores info about all connections
class surgeFactory(protocol.ServerFactory):
    protocol = SurgeChatProtocol

    #possible states and client types for chat server clients
    states = enum('REGISTER','IS_CLIENT','IS_SERVER','CHALLENGE_SERVER')
    clientTypes = enum('surgeserver', 'surgeclient')

    #number of clients that are currently connected to chat server
    client_count = 0

    #dictionary of connected clients, keys are user ids, values
    #are protocols that belong to the respective user connections
    connectedClients = {}

    #dictionary of currently active conversations between two clients
    #needed since its possible for a client to have multiple chat
    #instances open with different users, thus I need to make sure that
    #the conversationID and the message are sent to the recipient
    openConversations = {}


#create server and start listening on port 8000
endpoints.serverFromString(reactor, 'tcp:8000').listen(surgeFactory())

#start the reactor!
reactor.run()
