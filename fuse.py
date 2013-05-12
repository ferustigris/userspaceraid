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
import logging
import os
from collections import defaultdict
from llfuse import FUSEError

log = logging.getLogger()

class Operations(llfuse.Operations):
    def __init__(self):      
        self.inode = 1
        self.inodes = {1: ''}
        print("__init__")
        super(Operations, self).__init__()
        print("__init__")
    def lookup(self, inode_p, name):
        print("lookup %s", name)
        if name == '.':
            inode = inode_p
        else:
            inode = self.inode + 1
            self.inode = inode
            #path = self.inodes[inode_p] + "/" + name
            #print("lookup path=%s", path)
            #st = os.stat(path)
            #name == '..':
            #raise(llfuse.FUSEError(errno.ENOENT))
        
        return self.getattr(inode)
    def getattr(self, inode):
        print("getattr inode=", inode)
        entry = llfuse.EntryAttributes()
        entry.st_ino = inode
        entry.generation = 0
        entry.entry_timeout = 300
        entry.attr_timeout = 300
        entry.st_mode = 040777
        entry.st_nlink = 2
        entry.st_uid = 0
        entry.st_gid = 0
        entry.st_rdev = 1
        entry.st_size = 0

        entry.st_blksize = 512
        entry.st_blocks = 1
        entry.st_atime = 0
        entry.st_mtime = 0
        entry.st_ctime = 0
        return entry
    def readlink(self, inode):
        print("readlink")
        return self.get_row('SELECT * FROM inodes WHERE id=?', (inode,))['target']
    
    def opendir(self, inode):
        print("opendir ", inode)
        return inode

    def readdir(self, inode, off):
        print("readdir ", inode)
        if off == 0:
            off = -1
        for row in []:
            print(row, self.inode)
            self.inode = self.inode + 1
            yield (row, self.getattr(self.inode), self.inode)

    def unlink(self, inode_p, name):
        print("unlink")
        entry = self.lookup(inode_p, name)

        if stat.S_ISDIR(entry.st_mode):
            raise llfuse.FUSEError(errno.EISDIR)

        self._remove(inode_p, name, entry)

    def rmdir(self, inode_p, name):
        print("rmdir")
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
        print("open")
        return inode

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
        print("read")
        data = "no data"
        if data is None:
            data = ''
        return data[offset:offset+length]

                
    def write(self, fh, offset, buf):
        print("write")
        data = 'sadfsd'
        if data is None:
            data = ''
        data = data[:offset] + buf + data[offset+len(buf):]
        
        return len(buf)
   
    def release(self, fh):
        print("release")

        
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
    