#!/bin/env/python
import sys
from surgeUtilities import *
from twisted.internet import reactor, protocol, endpoints
from twisted.internet.defer import Deferred
from twisted.protocols import basic
import json


class SurgeTestClientProtocol(protocol.Protocol):
  senderID = random.randint(1,10)
  clientMessage = '{"clientType":"surgeclient" ,"messageType":"connect", "senderID":"'+ str(senderID) +'"}'

  def connectionMade(self):
    print 'client connected'
    self.transport.write(self.clientMessage)

  def connectionLost(self, reason):
    print 'connection has been lost'

  def dataReceived(self, line):
    print line
    msg = json.loads(line)
    print msg["message"]


class SurgeTestClientFactory(protocol.ClientFactory):
    protocol = SurgeTestClientProtocol
    
    def clientConnectionFailed(self, connector, reason):
      print 'connection failed'

    def clientConnectionLost(self, connector, reason):
      print 'connection lost'

clientEndpoint = endpoints.clientFromString(reactor, 'tcp:localhost:8000')
attempt = clientEndpoint.connect(SurgeTestClientFactory())

reactor.run()
