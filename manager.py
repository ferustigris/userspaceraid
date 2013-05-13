#!/usr/bin/env python
import os
import sys
import errno
import stat
import plugin_skelet
from webdav import WebDav

class Manager():
    def __init__(self):
        print("Manager: init")
        self.plugins = [
            WebDav("/home/asd/src"),
            WebDav("/home/asd/Pictures"),
        ]
        self.root = "/home/asd/src"
        self.inodes = {1: self.root}
        self.inode = 1;
        self.fh = 1;

    def lookup(self, inode_p, name):
        print("Manager: lookup inode=", inode_p, ", name=", name)
        inode = -1
        for plugin in self.plugins:
            try:
                lInode_p = plugin.getLocalByGlobalInode(inode_p)
                localInode = plugin.lookup(lInode_p, name)
                if inode < 0:
                    inode = self.inode + 1;
                plugin.saveInode(inode, localInode)
            except OSError, e:
                pass
            except plugin_skelet.FileNotFoundError, e:
                pass
        if inode < 0:
            raise OSError
        self.inode = inode
        return inode
    def getattr(self, inode):
        print("Manager: getattr")
        for plugin in self.plugins:
            try:
                return plugin.getattr(plugin.getLocalByGlobalInode(inode))
            except OSError, e:
                pass
            except plugin_skelet.FileNotFoundError, e:
                pass
        raise(OSError)
    def setattr(self, inode, attr):
        print("Manager: setattr")
        for plugin in self.plugins:
            try:
                return plugin.setattr(inode, attr)
            except OSError, e:
                pass
            except plugin_skelet.FileNotFoundError, e:
                pass
    def readdir(self, inode, off):
        print("Manager: readdir")
        resultList = []
        for plugin in self.plugins:
            try:
                lInode = plugin.getLocalByGlobalInode(inode)
                resultList = resultList + plugin.readdir(lInode, off)
            except OSError, e:
                pass
            except plugin_skelet.FileNotFoundError, e:
                pass
        print "resultList", resultList
        return resultList
    def opendir(self, inode):
        print("Manager: opendir ", inode)
        return inode
    def open(self, inode, flags):
        print("Manager: open")
        for plugin in self.plugins:
            try:
                lInode = plugin.getLocalByGlobalInode(inode)
                fh = plugin.open(lInode, flags)
                self.fh = self.fh + 1
                plugin.saveFh(self.fh, fh)
                return self.fh
            except OSError, e:
                pass
            except plugin_skelet.FileNotFoundError, e:
                pass
        raise(OSError)
    def read(self, fh, offset, length):
        print("Manager: read")
        data = ''
        for plugin in self.plugins:
            try:
                lfh = plugin.getLocalByGlobalFh(fh)
                data = plugin.read(lfh, offset, length)
            except OSError, e:
                pass
            except plugin_skelet.FileNotFoundError, e:
                pass
        return data              
    def write(self, fh, offset, buf):
        print("Manager: write")
        for plugin in self.plugins:
            try:
                lfh = plugin.getLocalByGlobalFh(fh)
                return plugin.write(lfh, offset, buf)
            except OSError, e:
                pass
            except plugin_skelet.FileNotFoundError, e:
                pass
        raise(OSError)
    def release(self, fh):
        print("Manager: release")
        for plugin in self.plugins:
            try:
                lfh = plugin.getLocalByGlobalFh(fh)
                plugin.release(lfh)
            except OSError, e:
                pass
            except plugin_skelet.FileNotFoundError, e:
                pass

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

