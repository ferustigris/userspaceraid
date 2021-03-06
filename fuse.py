#!/usr/bin/env python

from __future__ import division, print_function, absolute_import

import os
import sys
import llfuse
import errno
import stat
from time import time
from manager import Manager
import logging
from collections import defaultdict
from llfuse import FUSEError

log = logging.getLogger()

class Operations(llfuse.Operations):
    def __init__(self):      
        print("Operations: init")
        self.manager = Manager();
        super(Operations, self).__init__()
    def lookup(self, inode_p, name):
        print("Operations: lookup inode=", inode_p, ", name=", name)
        if name == '.':
            inode = inode_p
        else:
            try:
                inode = self.manager.lookup(inode_p, name)
            except OSError, e:
                if e.errno == errno.ENOENT:
                    print('Manager: path does not exist or is a broken symlink')
                raise(llfuse.FUSEError(errno.ENOENT))
        return self.getattr(inode)
    def getattr(self, inode):
        print("Operations: getattr inode=", inode)
        entry = llfuse.EntryAttributes()
        try:
            st = self.manager.getattr(inode)
            entry.st_ino = inode
            entry.generation = 0
            entry.entry_timeout = 0
            entry.attr_timeout = 0
            entry.st_mode = st.st_mode
            entry.st_nlink = st.st_nlink
            entry.st_uid = st.st_uid
            entry.st_gid = st.st_gid
            entry.st_rdev = st.st_rdev
            entry.st_size = st.st_size
            entry.st_blksize = st.st_blksize
            entry.st_blocks = st.st_blocks
            entry.st_atime = st.st_atime
            entry.st_mtime = st.st_mtime
            entry.st_ctime = st.st_ctime
        except OSError, e:
            if e.errno == errno.ENOENT:
                print('Operations: path does not exist or is a broken symlink')
            raise(llfuse.FUSEError(errno.ENOENT))
        return entry
    def setattr(self, inode, attr):
        print("Operations: setattr")
        self.manager.setattr(inode, attr)
        return self.getattr(inode)
    def readlink(self, inode):
        print("Operations: readlink")
        return self.manager.readlink(inode)
    def opendir(self, inode):
        print("Operations: opendir ", inode)
        return self.manager.opendir(inode)
    def readdir(self, inode, off):
        print("Operations: readdir inode=", inode, ", off=", off)
        if off == 0:
            off = -1
        list = self.manager.readdir(inode, off)
        for entry in list:
            off = off + 1
            if off > len(list):
                off = 0
                return
            attr = self.lookup(inode, entry)
            yield (entry, attr, attr.st_ino)
        off = 0

    def open(self, inode, flags):
        print("Operations: open")
        return self.manager.open(inode, flags)
    def read(self, fh, offset, length):
        print("Operations: read fh=", fh)
        return self.manager.read(fh, offset, length)
    def write(self, fh, offset, buf):
        print("Operations: write fh=", fh)
        return self.manager.write(fh, offset, buf)
    def release(self, fh):
        print("Operations: release fh=", fh)
        return self.manager.release(fh)

    def mkdir(self, inode_p, name, mode, ctx):
        print("Operations: mkdir")
        try:
            self.manager.mkdir(inode_p, name, mode)
        except OSError, e:
            raise llfuse.FUSEError(errno.ENOTDIR)
        return self.lookup(inode_p, name)
    def rmdir(self, inode_p, name):
        print("Operations: rmdir")
        entry = self.lookup(inode_p, name)
        if not stat.S_ISDIR(entry.st_mode):
            raise llfuse.FUSEError(errno.ENOTDIR)
        try:
            self.manager.rmdir(inode_p, name)
        except OSError, e:
            raise llfuse.FUSEError(errno.ENOTDIR)

    def create(self, inode_parent, name, mode, flags, ctx):
        print("Operations: create")
        fh = self.manager.create(inode_parent, name, mode, flags)
        return (fh, self.lookup(inode_parent, name))
    def unlink(self, inode_p, name):
        print("Operations: unlink")
        entry = self.lookup(inode_p, name)
        if stat.S_ISDIR(entry.st_mode):
            raise llfuse.FUSEError(errno.EISDIR)
        self.manager.unlink(entry.st_ino)
    def rename(self, inode_p_old, name_old, inode_p_new, name_new):     
        print("Operations: rename")
        entry_old = self.lookup(inode_p_old, name_old)
        try:
            entry_new = self.lookup(inode_p_new, name_new)
        except llfuse.FUSEError as exc:
            target_exists = False
        else:
            target_exists = True
            raise FUSEError(errno.EINVAL)
        self.manager.rename(inode_p_old, name_old, inode_p_new, name_new)

    def statfs(self):
        print("Operations: statfs")
        stat_ = llfuse.StatvfsData()
        st = self.manager.statfs()

        stat_.f_bsize = st.f_bsize
        stat_.f_frsize = st.f_frsize

        stat_.f_blocks = st.f_blocks
        stat_.f_bfree = st.f_bfree
        stat_.f_bavail = st.f_bavail

        stat_.f_files = st.f_files
        stat_.f_ffree = st.f_ffree
        stat_.f_favail = st.f_favail
        return stat_

    def symlink(self, inode_p, name, target, ctx):
        print("Operations: symlink")
        mode = (stat.S_IFLNK | stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | 
                stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP | 
                stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH)
        return self._create(inode_p, name, mode, ctx, target=target)
    def link(self, inode, new_inode_p, new_name):
        print("Operations: link")
        entry_p = self.getattr(new_inode_p)
        if entry_p.st_nlink == 0:
            raise FUSEError(errno.EINVAL)

        return self.getattr(inode)
    def mknod(self, inode_p, name, mode, rdev, ctx):
        print("Operations: mknod")
        return self._create(inode_p, name, mode, ctx, rdev=rdev)
    def access(self, inode, mode, ctx):
        print("Operations: access")
        return True

        
if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        raise SystemExit('Usage: %s <mountpoint>' % sys.argv[0])
    
    mountpoint = sys.argv[1]
    operations = Operations()
    
    llfuse.init(operations, mountpoint, [  b'fsname=tmpfs2' ])#, b"nonempty"
    
    try:
        llfuse.main(single=True)
    except:
        llfuse.close(unmount=False)
        raise

    llfuse.close()
    
