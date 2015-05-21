import random
import time
from twisted.internet import reactor, protocol, endpoints
from twisted.internet.defer import Deferred
from twisted.protocols import basic
import json


class SurgeTestClientProtocol(basic.LineReceiver):
  senderID = random.randint(1,10)
  clientMessage = '{"messageType":"surgeclient", "senderID":"'+ str(senderID) +'", "message":"a message!"}'

  def connectionMade(self):
    print 'client connected'
    self.sendLine(self.clientMessage)

  def connectionLost(self, reason):
    print 'connection has been lost'

  def lineReceived(self, line):
    print 'line received'
    print 'line:',line
    self.sendLine('message received by client.')
    self.sendLine(self.end)


class SurgeTestClientFactory(protocol.ClientFactory):
    protocol = SurgeTestClientProtocol
    
    def clientConnectionFailed(self, connector, reason):
      print 'connection failed'

    def clientConnectionLost(self, connector, reason):
      print 'connection lost'

clientEndpoint = endpoints.clientFromString(reactor, 'tcp:localhost:8000')
attempt = clientEndpoint.connect(SurgeTestClientFactory())

reactor.run()
