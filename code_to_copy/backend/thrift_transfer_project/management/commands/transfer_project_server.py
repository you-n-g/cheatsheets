#!/usr/bin/env python
#-*- coding:utf8 -*-

from django.core.management.base import NoArgsCommand, BaseCommand

from django.conf import settings

'''
import daemon #守护进程
import signal
signal.signal(signal.SIGCHLD, signal.SIG_IGN) #  如果没有这句话, 将会产程僵尸进程
'''

from thrift_transfer_project.server import run_server


class Command(BaseCommand):
    help = u"获取项目server"

    def handle(self, *args, **options):
        #with daemon.DaemonContext():
        run_server()
