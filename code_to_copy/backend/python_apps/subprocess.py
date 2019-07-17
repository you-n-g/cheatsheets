#!/usr/bin/env python
#-*- coding:utf8 -*-

import subprocess

# TODO: use communicate instead of PIPE
process = subprocess.Popen(["XXX_COMMAND", "XXX_ARGS"...], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, unused_err = process.communicate("XXX INPUT")  # this line include input, output, err info;
code = process.wait() # it will blocked here, otherwize it will run parallelly
