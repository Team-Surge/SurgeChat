import random
import time
from twisted.internet import reactor, protocol, endpoints
from twisted.internet.defer import Deferred
from twisted.protocols import basic
import json

#TODO: reorganize json fields (add clientType = server | client) and use messageType for Ack, Req, and Auth messages
class SurgeTestServerProtocol(protocol.Protocol):
    clientMessage = '{"clientType":"surgeserver", "messageType":"surgeserver", "serverToken":"", "conversationID":"", "senderID":"", "recipientID":"", "message":"Im totally the server"}'

    def connectionMade(self):
        print 'client connected'
        self.transport.write(self.clientMessage)

    def connectionLost(self, reason):
        print 'connection has been lost'

    def dataReceived(self, data):
        msg = json.loads(data)
        if 'challenge' in msg:
            print 'I HAZ BEEN CHALLENGED!'
            print 'challenge token:',msg["challenge"]
            challengeResponse = 'lol'
            self.transport.write('{"challengeResponse":"' + challengeResponse + '"}')
        else:
            print 'this is not a challenge'


class SurgeTestClientFactory(protocol.ClientFactory):
    protocol = SurgeTestServerProtocol
    
    def clientConnectionFailed(self, connector, reason):
      print 'connection failed'

    def clientConnectionLost(self, connector, reason):
      print 'connection lost'

clientEndpoint = endpoints.clientFromString(reactor, 'tcp:localhost:8000')
attempt = clientEndpoint.connect(SurgeTestClientFactory())

reactor.run()
