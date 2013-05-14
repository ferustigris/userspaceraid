#!/usr/bin/env python
import os
import stat
import abstract_backend
from posix_backend import PosixBackend

class Manager():
    def __init__(self):
        print("Manager: init")
        self.plugins = [
            PosixBackend("/home/asd/src"),
            PosixBackend("/home/asd/Pictures"),
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
            except abstract_backend.FileNotFoundError, e:
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
            except abstract_backend.FileNotFoundError, e:
                pass
        raise(OSError)
    def setattr(self, inode, attr):
        print("Manager: setattr")
        for plugin in self.plugins:
            try:
                return plugin.setattr(inode, attr)
            except OSError, e:
                pass
            except abstract_backend.FileNotFoundError, e:
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
            except abstract_backend.FileNotFoundError, e:
                pass
        return list(set(resultList))
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
            except abstract_backend.FileNotFoundError, e:
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
            except abstract_backend.FileNotFoundError, e:
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
            except abstract_backend.FileNotFoundError, e:
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
            except abstract_backend.FileNotFoundError, e:
                pass

    def mkdir(self, inode_p, name, mode):
        print("Manager: mkdir")
        for plugin in self.plugins:
            try:
                lInode_p = plugin.getLocalByGlobalInode(inode_p)
                plugin.mkdir(lInode_p, name, mode)
            except OSError, e:
                pass
            except abstract_backend.FileNotFoundError, e:
                pass
    def rmdir(self, inode_p, name):
        print("Manager: rmdir")
        for plugin in self.plugins:
            try:
                lInode_p = plugin.getLocalByGlobalInode(inode_p)
                plugin.rmdir(lInode_p, name)
            except OSError, e:
                pass
            except abstract_backend.FileNotFoundError, e:
                pass

    def create(self, inode_parent, name, mode, flags):
        print("Manager: create")
        exist = False
        for plugin in self.plugins:
            try:
                plugin.lookup(inode_parent, name)
                exist = True
            except OSError, e:
                pass
            except abstract_backend.FileNotFoundError, e:
                pass
        if exist:
            raise(OSError)
        for plugin in self.plugins:
            try:
                lInode_p = plugin.getLocalByGlobalInode(inode_parent)
                return plugin.create(lInode_p, name, mode, flags)
            except OSError, e:
                pass
            except abstract_backend.FileNotFoundError, e:
                pass
        raise(OSError)

    def unlink(self, inode):
        print("Manager: unlink")
        for plugin in self.plugins:
            try:
                lInode = plugin.getLocalByGlobalInode(inode)
                plugin.unlink(lInode)
            except OSError, e:
                pass
            except abstract_backend.FileNotFoundError, e:
                pass
    def rename(self, inode_p_old, name_old, inode_p_new, name_new):     
        print("Manager: rename")
        for plugin in self.plugins:
            try:
                lInodeOld_p = plugin.getLocalByGlobalInode(inode_p_old)
                lInodeNew_p = plugin.getLocalByGlobalInode(inode_p_new)
                plugin.rename(lInodeOld_p, name_old, lInodeNew_p, name_new)
            except OSError, e:
                pass
            except abstract_backend.FileNotFoundError, e:
                pass
    def statfs(self):
        print("Manager: statfs")
        class Employee:
            pass
        stat = None
        for plugin in self.plugins:
                st = plugin.statfs()
                if stat is None:
                    stat = Employee()
                    stat.f_bsize = st.f_bsize
                    stat.f_frsize = st.f_frsize

                    stat.f_blocks = st.f_blocks
                    stat.f_bfree = st.f_bfree
                    stat.f_bavail = st.f_bavail

                    stat.f_files = st.f_files
                    stat.f_ffree = st.f_ffree
                    stat.f_favail = st.f_favail
                else:
                    stat.f_blocks = stat.f_blocks + st.f_blocks
                    stat.f_bfree = stat.f_bfree + st.f_bfree
                    stat.f_files = stat.f_files + st.f_files
                    stat.f_ffree = stat.f_ffree + st.f_ffree
                    stat.f_favail = stat.f_favail + st.f_favail
                    stat.f_bavail = stat.f_bavail + st.f_bavail
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

