# _*_ coding: utf-8 _*_
'''
    https://zoink.it
'''

import urllib, urllib2, os, MySQLdb, gzip
from io import BytesIO
from Parser import Parser
from Browser import BrowserBase
from binascii import a2b_hex
import hashlib

def get_download_url(hash):
    b = a2b_hex(hash.lower())
    sha = hashlib.sha1()
    sha.update(b"bc" + b + b"torrent")
    print(sha.hexdigest())

def getTorrents(info_hash):
    infohash = info_hash.upper()
    # url="http://torcache.net/torrent/%s.torrent"%info_hash.upper()
    url = "http://bt.box.n0808.com/%s/%s/%s.torrent" % (infohash[:2], infohash[len(infohash) - 2:], infohash)
    print url

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
        }
        req = urllib2.Request(
            url=url,
            headers=headers
        )
        torrent = urllib2.urlopen(req, timeout=10).read()
        #         buffer = BytesIO(torrent)
        #         gz = gzip.GzipFile(fileobj=buffer)
        #         raw_data=gz.read()
        parser = Parser(torrent)
        print parser.getName()
        print parser.getFiles()
        print parser.getFileCount()
        print parser.getFileSize()
    except IOError, e:
        print e
        # print "downloading+"+info_hash+".torrent failed"
        return False
    # print "downloading+"+info_hash+".torrent success"
    return True


if __name__ == "__main__":
    get_download_url("004f50950256e66f128d528d0773fdefbc298cce")
