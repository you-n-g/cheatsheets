#!/usr/bin/env python
#-*- coding:utf8 -*-

class P3PMiddleware(object):
    def process_response(self, request, response):
        # 如果不设置这个header， IE会不信任你的网站，导致无法保留 cookies
        response["P3P"] = 'CP="NOI ADM DEV COM NAV OUR STP"'
        return response
