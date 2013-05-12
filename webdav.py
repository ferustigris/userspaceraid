#!/usr/bin/env python
import os
import sys
import errno
import stat
from plugin_skelet import PluginSkelet

class WebDav(PluginSkelet):
    def __init__(self, root):
        print("Manager: init, root=", root)
        super(WebDav, self).__init__()
        self.root = root
        self.inodes = {1: self.root}
        self.saveInode(1, 1)

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
    def setattr(self, inode, attr):
        print("Manager: setattr=", attr.st_mode)
        path = self.inodes[inode]
        if attr.st_mode is not None:
            os.chmod(path, attr.st_mode)
        if attr.st_uid is not None and attr.st_gid is not None:
            os.chown(path, attr.st_uid, attr.st_gid)
        if attr.st_atime is not None and attr.st_mtime is not None:
            os.utime(path, (attr.st_atime, attr.st_mtime))
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
        return os.write(fh, buf)
    def release(self, fh):
        print("Manager: release")
    	os.close(fh)

    def mkdir(self, inode_p, name, mode):
        print("Manager: mkdir")
        path = os.path.join(self.inodes[inode_p], name)
        os.mkdir(path, mode)
    def rmdir(self, inode_p, name):
        print("Manager: rmdir")
        path = os.path.join(self.inodes[inode_p], name)
        return os.rmdir(path)

    def create(self, inode_parent, name, mode, flags):
        print("Manager: create")
        path = os.path.join(self.inodes[inode_parent], name)
        return os.open(path, flags)
    def unlink(self, inode):
        print("Manager: unlink")
        path = self.inodes[inode]
        os.unlink(path)
    def rename(self, inode_p_old, name_old, inode_p_new, name_new):     
        print("Manager: rename")
        oldpath = os.path.join(self.inodes[inode_p_old], name_old)
        newpath = os.path.join(self.inodes[inode_p_new], name_new)
        os.rename(oldpath, newpath)
        inode = self.lookup(inode_p_new, name_new)
        self.inodes[inode] = newpath

    def statfs(self):
        print("Manager: statfs")
        stat = os.statvfs(self.root)
        return stat

    def readlink(self, inode):
        print("Manager: readlink")
        return inode
    def symlink(self, inode_p, name, target, ctx):
        print("Manager: symlink")
    def link(self, inode, new_inode_p, new_name):
        print("Manager: link")
    def mknod(self, inode_p, name, mode, rdev, ctx):
        print("Manager: mknod")
    def access(self, inode, mode, ctx):
        print("Manager: access")
        return True

