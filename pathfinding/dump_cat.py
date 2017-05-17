#!/usr/bin/python
# Copyright (c) 2009 Denis Bilenko. See LICENSE for details.

"""Spawn multiple workers and wait for them to complete"""
import gevent
from gevent import monkey
from gevent.pool import Pool
from gevent import Timeout
# patches stdlib (including socket and ssl modules) to cooperate with other greenlets
monkey.patch_all()

import csv
import logging
import sys
import os
from urllib2 import urlopen, URLError, HTTPError





def dlfile(url,downloaded_set):
    # Open the url
    try:

        timeout = Timeout(60)
        timeout.start()

        url_str = url.encode('utf-8')
        f = urlopen(url_str)
        #print("downloading " + url)
        # Open our local file for writing
        with open('out/' + os.path.basename(url_str), "wb",0) as local_file:
            local_file.write(f.read())
            downloaded_set.add(url)

    #handle errors
    except HTTPError, e:
        print("HTTP Error:", e.code, url)
    except URLError, e:
        print("URL Error:", e.reason, url)
    except Timeout:
        #print('Timeout')
        pass
    except:
        pass
    finally:
        timeout.cancel()

count = 0


while(1):
    print(count)
    with open('downloaded_data.csv', 'a+') as downloaded_fp:
        downloaded_fp.seek(0,0)
        reader=csv.reader(downloaded_fp,)
        downloaded_uris = set([unicode(x[0],'utf-8') for x in reader])

    with open('data_to_download.csv','r') as uris_fp:
        reader=csv.reader(uris_fp,)
        uris = set([unicode(x[0],'utf-8') for x in reader])

    to_download_uri = uris - downloaded_uris
    if(len(to_download_uri)) == 0:
        print('no more file to download')
        sys.exit()

    CONCURRENCY = 100 # run 200 greenlets at once or whatever you want
    pool = Pool(CONCURRENCY)
    

    for uri in list(to_download_uri)[:10000]:
        count += 1 # for logging purposes to track progress
        logging.info(count)
        pool.spawn(dlfile,uri,downloaded_uris) # blocks here when pool size == CONCURRENCY  
    pool.join() #blocks here until the last 200 are complete
    with open('downloaded_data.csv','wb',0) as downloaded_fp:
        csv_out=csv.writer(downloaded_fp,)
        for row in downloaded_uris:
            row_utf8 = row.encode('utf-8')
            csv_out.writerow([row_utf8])