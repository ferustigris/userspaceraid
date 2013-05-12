#!/usr/bin/env python

from __future__ import division, print_function, absolute_import

import os
import sys

# We are running from the llfuse source directory, make sure
# that we use modules from this directory
basedir = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..'))

if (os.path.exists(os.path.join(basedir, 'setup.py')) and
    os.path.exists(os.path.join(basedir, 'src', 'llfuse.pyx'))):
    sys.path = [os.path.join(basedir, 'src')] + sys.path
    
    
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

    def unlink(self, inode_p, name):
        print("Operations: unlink")
        entry = self.lookup(inode_p, name)

        if stat.S_ISDIR(entry.st_mode):
            raise llfuse.FUSEError(errno.EISDIR)

        self._remove(inode_p, name, entry)

    def rmdir(self, inode_p, name):
        print("Operations: rmdir")
        entry = self.lookup(inode_p, name)

        if not stat.S_ISDIR(entry.st_mode):
            raise llfuse.FUSEError(errno.ENOTDIR)

        self._remove(inode_p, name, entry)

    def _remove(self, inode_p, name, entry):
        print("_remove")

    def symlink(self, inode_p, name, target, ctx):
        print("symlink")
        mode = (stat.S_IFLNK | stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | 
                stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP | 
                stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH)
        return self._create(inode_p, name, mode, ctx, target=target)

    def rename(self, inode_p_old, name_old, inode_p_new, name_new):     
        print("rename")
        entry_old = self.lookup(inode_p_old, name_old)

        try:
            entry_new = self.lookup(inode_p_new, name_new)
        except llfuse.FUSEError as exc:
            if exc.errno != errno.ENOENT:
                raise
            target_exists = False
        else:
            target_exists = True


    def link(self, inode, new_inode_p, new_name):
        print("link")
        entry_p = self.getattr(new_inode_p)
        if entry_p.st_nlink == 0:
            raise FUSEError(errno.EINVAL)

        return self.getattr(inode)

    def setattr(self, inode, attr):
        print("setattr")
        return self.getattr(inode)

    def mknod(self, inode_p, name, mode, rdev, ctx):
        print("mknod")
        return self._create(inode_p, name, mode, ctx, rdev=rdev)

    def mkdir(self, inode_p, name, mode, ctx):
        print("mkdir")
        return self._create(inode_p, name, mode, ctx)

    def statfs(self):
        print("statfs")
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

    def open(self, inode, flags):
        print("Operations: open")
        return self.manager.open(inode, flags)

    def access(self, inode, mode, ctx):
        print("access")
        return True

    def create(self, inode_parent, name, mode, flags, ctx):
        print("create")
        entry = self._create(inode_parent, name, mode, ctx)
        return (entry.st_ino, entry)

    def _create(self, inode_p, name, mode, ctx, rdev=0, target=None):             
        print("_create")
        if self.getattr(inode_p).st_nlink == 0:
            raise FUSEError(errno.EINVAL)

        return self.getattr(inode)


    def read(self, fh, offset, length):
        print("Operations: read fh=", fh)
        return self.manager.read(fh, offset, length)
                
    def write(self, fh, offset, buf):
        print("Operations: write fh=", fh)
        data = 'sadfsd'
        if data is None:
            data = ''
        data = data[:offset] + buf + data[offset+len(buf):]
        
        return len(buf)
   
    def release(self, fh):
        print("Operations: release fh=", fh)
        return self.manager.release(fh)

        
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
    
