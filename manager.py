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
        return os.listdir(path)
    def opendir(self, inode):
        print("Manager: opendir ", inode)
        return inode
    def open(self, inode, flags):
        print("Manager: open")
        path = self.inodes[inode]
        fh = os.open(path, flags)
        return fh
    def read(self, fh, offset, length):
        print("Manager: read")
        os.lseek(fh, offset, os.SEEK_SET)
        data = os.read(fh, length)
        if data is None:
            data = ''
        return data              
    def write(self, fh, offset, buf):
        print("Manager: write")
        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, buf, len(buf))
    def release(self, fh):
        print("Manager: release")
    	os.close(fh)

    def mkdir(self, inode_p, name, mode):
        print("Manager: mkdir")
        path = os.path.join(self.inodes[inode_p], name)
        os.mkdir(path, mode)


    def statfs(self):
        print("Manager: statfs")
        stat_ = llfuse.StatvfsData()

        stat_.f_bsize = 512
        stat_.f_frsize = 512

        size = 12
        stat_.f_blocks = size // stat_.f_frsize
        stat_.f_bfree = max(size // stat_.f_frsize, 1024)
        stat_.f_bavail = stat_.f_bfree

        inodes = 0
        stat_.f_files = inodes
        stat_.f_ffree = max(inodes , 100)
        stat_.f_favail = stat_.f_ffree

        return stat_
    def readlink(self, inode):
        print("Manager: readlink")
        return inode
    def unlink(self, inode_p, name):
        print("Manager: unlink")

    def symlink(self, inode_p, name, target, ctx):
        print("Manager: symlink")

    def rename(self, inode_p_old, name_old, inode_p_new, name_new):     
        print("Manager: rename")

    def link(self, inode, new_inode_p, new_name):
        print("Manager: link")

    def setattr(self, inode, attr):
        print("Manager: setattr")

    def mknod(self, inode_p, name, mode, rdev, ctx):
        print("Manager: mknod")

    def access(self, inode, mode, ctx):
        print("Manager: access")
        return True

    def create(self, inode_parent, name, mode, flags, ctx):
        print("Manager: create")
        entry = self._create(inode_parent, name, mode, ctx)
        return (entry.st_ino, entry)
