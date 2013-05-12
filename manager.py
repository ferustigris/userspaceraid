#!/usr/bin/env python
import os
import sys
import errno
import stat

class Manager():
    def __init__(self):
        print("Manager: init")
        self.inodes = {1: "/home/asd/src"}

    def lookup(self, inode_p, name):
        print("Manager: lookup inode=", inode_p, ", name=", name)
        if name == '.':
            inode = inode_p
        else:
            path = os.path.join(self.inodes[inode_p], name)
            print("Manager: lookup path=%s", path)
            st = os.stat(path)
            inode = st.st_ino
            self.inodes[inode] = path
        return inode
    def getattr(self, inode):
        path = self.inodes[inode]
        print("Manager: getattr inode=", inode, ", path=", path)
        try:
            return os.stat(path)
        except OSError, e:
            if e.errno == errno.ENOENT:
                print('Manager: path %s does not exist or is a broken symlink', path)
            raise(llfuse.FUSEError(errno.ENOENT))
    def readdir(self, inode, off):
        path = self.inodes[inode]
        print("Manager: readdir inode=", inode, ", path=", path, ", off=", off)
        list = os.listdir(path)
        return list
    def readlink(self, inode):
        print("Manager: readlink")
        return self.get_row('SELECT * FROM inodes WHERE id=?', (inode,))['target']    
    def opendir(self, inode):
        print("Manager: opendir ", inode)
        return inode
