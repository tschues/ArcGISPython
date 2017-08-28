# -*- coding: UTF-8 -*-
from os.path import basename
from urlparse import urlsplit
import urllib2

def down_file():
    url = "http://sentinel-s2-l1c.s3-website.eu-central-1.amazonaws.com/#tiles/49/R/EP/2017/2/27/0/metadata.xml"
    file_name = url.split('/')[-1]
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        file_size_dl += len(buffer)
        f.write(buffer)
    f.close()  

def url2name(url):
    return basename(urlsplit(url)[2])
def download(url, localFileName = None):
    localName = url2name(url)
    print localName
    req = urllib2.Request(url)
    r = urllib2.urlopen(req)
    if r.info().has_key('Content-Disposition'):
        # If the response has Content-Disposition, we take file name from it
        localName = r.info()['Content-Disposition'].split('filename=')[1]
        if localName[0] == '"' or localName[0] == "'":
            localName = localName[1:-1]
    elif r.url != url:
        # if we were redirected, the real file name we take from the final URL
        localName = url2name(r.url)
        if localFileName:
            # we can force to save the file as specified name
            localName = localFileName
            
            f = open(localName, 'wb')
            f.write(r.read())
            f.close()
            
download(r'http://sentinel-s2-l1c.s3-website.eu-central-1.amazonaws.com/#tiles/49/R/EP/2017/2/27/0/metadata.xml')
