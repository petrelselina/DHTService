# -*- coding: utf-8 -*-
from bencode import bdecode


class Parser(object):
    def __init__(self, fileinfo):

        self.metainfo = bdecode(fileinfo)
        self.info = self.metainfo["info"]
        print self.metainfo

    def getName(self):
        info = self.info
        if 'name.utf-8' in info:
            filename = info['name.utf-8']
        else:
            filename = info['name']

        for c in filename:
            if c == "'":
                filename = filename.replace(c, "\\\'")
        return filename

    def getEncoding(self):
        if 'encoding' in self.metainfo:
            return self.metainfo['encoding']
        return ""

    def getComments(self):
        info = self.info

        if 'comment.utf-8' in self.metainfo:
            comment = self.metainfo['comment.utf-8']
            return comment
        else:
            return ''

    def getObject(self):
        info = self.metainfo['info']

    def getFiles(self):
        if "files" in self.info:
            return self.info["files"]
        else:
            return []

    def getFileCount(self):
        return len(self.getFiles())

    def getFileSize(self):
        files = self.getFiles()
        size = 0
        for f in files:
            size += f["length"]
        return size
