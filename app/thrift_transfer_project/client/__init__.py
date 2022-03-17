#!/usr/bin/env python
#-*- coding:utf8 -*-

from thrift.transport import TTransport
from thrift.transport import TSocket
from thrift.protocol import TBinaryProtocol

from thrift_transfer_project.transfer_project_interface import GetProject
from thrift_transfer_project.transfer_project_interface.ttypes import *

from django.conf import settings


CLIENT_TRANSFER_PROJECT_HOST = getattr(settings, 'CLIENT_TRANSFER_PROJECT_HOST', '127.0.0.1')
CLIENT_TRANSFER_PROJECT_PORT = getattr(settings, 'CLIENT_TRANSFER_PROJECT_PORT', '9090')

class OpenClient(object):
    """
    用法
    with OpenClient() as client:
        do something with client....
    """
    def __init__(self):
        socket = TSocket.TSocket(CLIENT_TRANSFER_PROJECT_HOST, CLIENT_TRANSFER_PROJECT_PORT)
        self.transport = TTransport.TBufferedTransport(socket)
        protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.client = GetProject.Client(protocol)

    def __enter__(self):
        self.transport.open()
        return self.client
    
    def __exit__(self, *args, **kwargs):
        self.transport.close()
