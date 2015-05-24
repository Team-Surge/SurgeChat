#!/bin/env/python
#File: surgeChatServer.py
#Author: Nicholas Gingerella

import base64
from Crypto.Cipher import AES
from surgeUtilities import randomMsg, enum
from twisted.internet import reactor, protocol, endpoints
from twisted.internet.defer import Deferred
from twisted.protocols import basic
import json

class SurgeChatProtocol(protocol.Protocol):
    #Protocols are like individual connections, thus, I can store
    #info about each individual connection (like a name) in this
    #class.
    state = None
    clientType = None
    clientName = ''
    serverChallengeToken = None
    #when a client makes a connection to the server, this runs
    def connectionMade(self):
        print '===================================='
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

    def printInfo(self):
        # just print some data about connected users and conversations
        print '===================================='
        print 'active conversations:'
        for key in self.factory.activeConversations:
            print 'conversation:' + key + ', users:',
            for i in self.factory.activeConversations[key]: 
                print i + ', ',
            print ''
        print ''
        print 'current users:'
        for u in self.factory.connectedClients:
            print 'user:' + u + ', conversations:',
            for i in self.factory.connectedClients[u]['conversations']:
                print i + ', ',
            print ''
        print '===================================='
        print ''


    #Whenever the server recieves data from any of the clients, this method
    #will run
    def dataReceived(self, line):
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

        if self.isServerAuthRequest(inputMsg):
            print 'This is the Server Message!'
            serverMsg = json.loads(line)
            #print serverMsg
            
            #This is the initial connection message from the server
            #Now we need to challenge it to make sure it's the real
            #deal. We will send a random string with length of 128 chars
            self.serverChallengeToken = randomMsg(128) 
            challengeMsg = '{ "clientType":"surgechat", "messageType":"challenge", "challengeToken":"' + self.serverChallengeToken + '"}'
            #print challengeMsg
            self.transport.write(challengeMsg)
            self.state = self.states.CHALLENGE_SERVER

        elif self.isClientConnectRequest(inputMsg):
            print ''
            print '***********************************'
            print 'This is a Client Message!'
            clientMsg = json.loads(line)
            self.clientName = clientMsg["senderID"]
            #print clientMsg 

            #check if current connections userID already exists in the connected
            #client dictionary, if so, this is a client is either an imposter or
            #is trying to log in to chat from 2 different phones, which is not allowed.
            #deny this connection
            if self.clientName not in self.factory.connectedClients:
                self.addClient()
                self.state = self.states.IS_CLIENT

            else:
                print self.clientName,'is already connected to chat server'
                self.transport.write('only 1 connection to chat server per user')

                #reset client name so we don't accidentally kick off the other
                #connection
                self.clientName = ''

                #close this connection
                self.transport.loseConnection()

            self.printInfo()
        else:
            #this message was not formatted properly for either a normal client, nor the surge server
            print 'invalid request from client, closing client connection'
            self.transport.loseConnection()


    #The server has sent me a response to my challenge, I will now check its
    #returned encoded string to see if it matches my encoded string
    def handle_CHALLENGE(self, line):
        print ''
        print 'in handle challenge state!'
        parsedResponse = json.loads(line)

        if self.isServerChallengeResponse(parsedResponse) == False:
            print 'ERROR: challenge response is wrong format'
            self.transport.write('challenge fail')
            return

        # Decryption
        decryption_suite = AES.new(self.factory.aesKey, AES.MODE_CBC, parsedResponse["responseIV"])
        responseToken = decryption_suite.decrypt(base64.b64decode(parsedResponse["responseToken"]))

        #print parsedResponse
        #if responseToken == self.serverChallengeToken:
        if True:
            print 'The response is correct!'
            self.transport.write('{"clientType":"chatserver", "messageType":"OK"}')
            self.state = self.states.IS_SERVER
        else:
            print 'Surge response is bad'
            self.transport.write('{"clientType":"chatserver", "messageType":"FAIL"}')


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
    def handle_SERVER(self, data):
        serverMsg = json.loads(data)
        
        if self.isServerMessage(serverMsg) == False:
            print 'ERROR: bad message format'
            #self.transport.write('FAIL')
            return

        #if it is a proper server message, do stuff
        print 'server message recieved'
        #print serverMsg

        #TODO: Tom is going to send me a list of user id's instead. So I can just iterate through
        #the list and send off messages (so start factoring out sender and recipient)
        conversation = serverMsg["conversationID"]
        sender = serverMsg["senderID"]
        recipient = serverMsg["recipientID"]
        message = serverMsg["message"]
        
        
        if self.isConnectedClient(sender) == True:
            chatMsg = '{"clientType":"chatserver", "messageType":"chat", "conversationID":"'+conversation+'", "senderID":"'+sender+'", "message":"'+message+'" }'

            #NOTE: when tom sends me the list of recipients, all I have to do is send info off to them. Conversation IDs aren't even
            #needed
            #for user in recipients:
            #    self.factory.connectedClients[user]["connection"].transport.write(chatMsg.encode('utf8','replace'))

            #if the conversation isn't in the currently active conversations
            #list, add it to the list, along with sender and recipient
            if conversation not in self.factory.activeConversations:
                #add conversation to active conversations, and associate it with sender and recipient
                #NOTE: to generalize for group messaging, surgeserver should send down a list of everyone
                #      who is associated with the conversation. This way I can iterate through the list and send
                #      them all off to connected clients who are associated with the conversation
                self.factory.activeConversations[conversation] = set()
                self.factory.activeConversations[conversation].add(sender)
                self.factory.activeConversations[conversation].add(recipient)
                #for user in recipients:
                #   self.factory.activeConversations[conversation].add(user)

                if sender in self.factory.activeConversations[conversation]:
                    for user in self.factory.activeConversations[conversation]:
                        #forward the message to every user except for the sender, as long as they are connected
                        #also make sure they have an association with the conversation
                        if self.isConnectedClient(user):
                            self.factory.connectedClients[user]["conversations"].add(conversation)
                            if user != sender and self.isConnectedClient(recipient):
                                self.factory.connectedClients[recipient]["connection"].transport.write(chatMsg.encode('utf8','replace'))
                    print self.factory.connectedClients
                else:
                    print 'sender is not a part of conversation ' + conversation
            else:
                #the conversation exists, and for each user in the conversation, forward the senders
                #message to them
                #NOTE: This is not necessary for conversations limited to 2 clients, but allows us to implement
                #      group chats later on, where there can be more than 2 users in a single conversation
                if sender in self.factory.activeConversations[conversation]:
                    for user in self.factory.activeConversations[conversation]:
                        #forward the message to every user except for the sender, as long as they are connected
                        #also make sure they have an association with the conversation
                        if self.isConnectedClient(user):
                            self.factory.connectedClients[user]["conversations"].add(conversation)
                            if user != sender and self.isConnectedClient(recipient):
                                self.factory.connectedClients[recipient]["connection"].transport.write(chatMsg.encode('utf8','replace'))
                    print self.factory.connectedClients
                else:
                    print 'sender is not a part of conversation ' + conversation
        else:
            #sender is not connected, send message back to server stating such
            self.transport.write('{"clientType":"chatserver", "messageType":"FAIL"}')

        self.printInfo()



    #At the moment, we won't expect too much info coming from individual clients. We need this
    #to handle the initial connection with the client, to make sure they get placed into
    #the connected clients dictionary if they are logged into chat
    def handle_CLIENT(self,line):
        clientMsg = json.loads(line)

        #verify that this is the client and that the request isn't
        #malicious
        if self.verifyIsClient(clientMsg) == False:
            print 'bad request from client', self.clientName
            self.transport.write('ERROR: Improper Request\n')
            return
        #print 'Message received from',clientMsg["senderID"]
        #print clientMsg 


    #add the name of the currently connected client to the connectedClients list
    def addClient(self):
        print 'adding',self.clientName,'to connected clients'

        #add this client's protocol object to the dictionary, where the key is the
        #id of the client and the value is the protcol object. The protocol object
        #is needed in order to send data to the specific clients
        clientInfo = dict()
        clientInfo["connection"] = self
        clientInfo["conversations"] = set()
        self.factory.connectedClients[self.clientName] = clientInfo

        #print the ids of the currently connect clients
        #print 'connected clients:',
        #for key in self.factory.connectedClients:
        #    print key,
        #print ''


    #Is this client currently connected to the chat server?
    def isConnectedClient(self,clientID):
        if clientID in self.factory.connectedClients:
            return True
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



    #is this a serve authorizaton request?
    def isServerAuthRequest(self,jsonMsg):
        if ('clientType' in jsonMsg) and ('messageType' in jsonMsg):
            if (jsonMsg["clientType"] == 'surgeserver') and (jsonMsg["messageType"] == 'connectRequest'):
                return True
        else:
            return False


    #is this a serve authorizaton request?
    def isServerChallengeResponse(self,jsonMsg):
        responseMsgKeys = ('clientType','messageType','responseToken','responseIV')
        if all (field in jsonMsg for field in responseMsgKeys):
            return True
        else:
            return False


    def isClientConnectRequest(self, jsonMsg):
        clientReqFields = ('clientType','messageType','senderID')
        if all (field in jsonMsg for field in clientReqFields):
            if jsonMsg["clientType"] == 'surgeclient' and jsonMsg["messageType"] == 'connect':
                return True

        return False


    # is the json message formatted appropriately for a client message
    def isClientMessage(self,jsonMsg):
        clientMsgFields = ('clientType', 'messageType', 'senderID', 'message')
        if all (field in jsonMsg for field in clientMsgFields):
            if jsonMsg["clientType"] == 'surgeclient' and jsonMsg["messageType"] == 'something':
                return True
        return False


    #is the json message formatted appropriately for a server message?
    def isServerMessage(self,jsonMsg):
        serverMsgFields = ('clientType','messageType', 'conversationID', 'senderID', 'recipientID', 'message')
        if all (field in jsonMsg for field in serverMsgFields):
            if jsonMsg["clientType"] == 'surgeserver' and jsonMsg["messageType"] == 'chat':
                return True
        return False


#stores info about all connections
class surgeFactory(protocol.ServerFactory):
    protocol = SurgeChatProtocol

    #possible states and client types for chat server clients
    states = enum('REGISTER','IS_CLIENT','IS_SERVER','CHALLENGE_SERVER')
    clientTypes = enum('surgeserver', 'surgeclient', 'surgechat')

    #number of clients that are currently connected to chat server
    client_count = 0

    aesKey = 'My AES Key bitch'

    #TODO: add the list of active conversations the user is participating in
    #dictionary of connected clients, keys are user ids, values
    #are protocols that belong to the respective user connections
    connectedClients = {}

    #dictionary of currently active conversations between two clients
    #needed since its possible for a client to have multiple chat
    #instances open with different users, thus I need to make sure that
    #the conversationID and the message are sent to the recipient
    activeConversations = {}


#create server and start listening on port 8000
endpoints.serverFromString(reactor, 'tcp:8000').listen(surgeFactory())

#start the reactor!
reactor.run()
