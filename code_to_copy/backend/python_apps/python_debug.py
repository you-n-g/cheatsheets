#!/usr/bin/env python
#-*- coding:utf8 -*-



# BEGIN PDB
# https://docs.python.org/2/library/pdb.html
import pdb

pdb.set_trace()
(Pdb) p a  # 即打印a
# END   PDB



# BEGIN traceback
import traceback
for line in traceback.format_stack():
    print line
# END   traceback
