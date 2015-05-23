import base64
from Crypto.Cipher import AES
from surgeUtilities import *
from twisted.internet import reactor, protocol, endpoints
from twisted.internet.defer import Deferred
from twisted.protocols import basic
import json

class SurgeTestServerProtocol(protocol.Protocol):
    clientMessage = '{"clientType":"surgeserver", "messageType": "connectRequest"}'

    def connectionMade(self):
        print 'client connected'
        self.transport.write(self.clientMessage)

    def connectionLost(self, reason):
        print 'connection has been lost'

    def dataReceived(self, data):
        print ''
        print 'received a message!'
        msg = json.loads(data)

        #check if all required fields are in the message
        challengeMsgKeys = ('clientType', 'messageType', 'challengeToken')
        if all (field in msg for field in challengeMsgKeys):
          if (msg['clientType'] == 'surgechat') and (msg['messageType'] == 'challenge'):
            print 'I HAZ BEEN CHALLENGED!'
            print 'challenge token:',msg["challengeToken"]

            #do the AES encryption on the received challengeToken
            aesIV = randomMsg(16)
            encryption_suite = AES.new(self.factory.aesKey, AES.MODE_CBC, aesIV)
            cipherText = encryption_suite.encrypt(msg["challengeToken"])
            b64cipherText = base64.b64encode(cipherText)

            challengeResponse = '{"clientType":"surgeserver", "messageType":"challengeResponse", "responseToken":"' + b64cipherText + '", "responseIV":"' + aesIV + '"}'
            print challengeResponse
            self.transport.write(challengeResponse)
        else:
          print(msg)
          



class SurgeTestClientFactory(protocol.ClientFactory):
    protocol = SurgeTestServerProtocol
    aesKey = 'My AES Key bitch'
    
    def clientConnectionFailed(self, connector, reason):
      print 'connection failed'

    def clientConnectionLost(self, connector, reason):
      print 'connection lost'

clientEndpoint = endpoints.clientFromString(reactor, 'tcp:localhost:8000')
attempt = clientEndpoint.connect(SurgeTestClientFactory())

reactor.run()
