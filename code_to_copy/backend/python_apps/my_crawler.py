#!/usr/bin/env python
#-*- coding:utf8 -*-

import os
import urllib2
import socket
import requests
from functools import partial
from multiprocessing import Pool
import shutil
import time

res_dir = 'reports'

TIMEOUTS = [5, 10, 20, 30, 40, 60, 120]
SLEEP = [5, 10, 20, 30, 40, 60, 120]

def download_report(url, fpath, tid):

    # Check if file is corrupted
    # if os.path.exists(fpath) and os.path.getsize(fpath) < 2000:
    #     print 'Clean corrupted file.'
    #     os.remove(fpath)

    if os.path.exists(fpath):
        print "%s alreadly exists.." % fpath
    else:
        downloading_path = fpath + '.downloading'
        print "Downloading from %s ...." % url
        dir_path = os.path.dirname(downloading_path)
        try:
            # this is done because of parallel running will download
            os.makedirs(dir_path)
        except OSError:
            # File exists already
            pass

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        }
        timeout_idx = 0
        sleep_idx = 0

        while True:
            try:
                resp = requests.get(
                    url, headers=headers, timeout=TIMEOUTS[timeout_idx % len(TIMEOUTS)])
                data = resp.content
                break
            except requests.exceptions.Timeout:
                print 'timeout... %s' %  url
                timeout_idx += 1
            except requests.exceptions.ConnectionError:
                print 'ConnectionError.. %s' % url
                time.sleep(SLEEP[sleep_idx % len(SLEEP)])
                sleep_idx += 1

        with open(downloading_path, 'wb') as f:
            f.write(data)

        shutil.move(downloading_path, fpath)
        print 'Downloaded %s, tid=%d' % (fpath, tid)


if __name__ == '__main__':
    # get tasks
    pool = Pool(40)
    res = []
    tid = 0
    for url in SOMETHING:
        fpath = SOMETHING
        kwargs = {
            'tid': tid,
            'url': url,
            'fpath': fpath,
        }
        # download_data(**kwargs)
        res.append((tid, pool.apply_async(download_data, [], kwargs)))
        tid += 1
    for i, r in res:
        try:
            print 'task (%d / %d) ended: ' % (i, tid), r.get()
        except Exception, e:
            print u"Type=%s, Args=%s" % (type(e), e.args)
    # pool.close() # TODO: If I put it before r.get(). The print info above will never output the data.
    # pool.join() # TODO: one must call close before call join
