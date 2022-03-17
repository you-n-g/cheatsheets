#!/usr/bin/env python
#-*- coding:utf8 -*-

from thrift_transfer_project.transfer_project_interface import GetProject
from thrift_transfer_project.transfer_project_interface.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from django.conf import settings

SERVER_TRANSFER_PROJECT_HOST = getattr(settings, 'SERVER_TRANSFER_PROJECT_HOST', '127.0.0.1')
SERVER_TRANSFER_PROJECT_PORT = getattr(settings, 'SERVER_TRANSFER_PROJECT_PORT', '9090')


class TransferProjectHandler(object):
    def xxx_function(self, pk):
        raise ProjectException(404, "project_not_found")
        return Project()

def run_server():
    handler = TransferProjectHandler()
    processor = GetProject.Processor(handler)
    transport = TSocket.TServerSocket(SERVER_TRANSFER_PROJECT_HOST, SERVER_TRANSFER_PROJECT_PORT)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
    server.serve()
