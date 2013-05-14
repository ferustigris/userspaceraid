#!/usr/bin/env python
import os
import sys
import errno
import stat
from abc import *

class FileNotFoundError:
    def __str__(self):
        return 'File not found'

class AbstractBackend(object):
    def __init__(self):
        print("AbstractBackend: init")
        self.inodesMap = {}
        self.fhMap = {}

    def saveInode(self, globalInode, localInode):
        self.inodesMap[globalInode] = localInode
    def getLocalByGlobalInode(self, globalInode):
        if not globalInode in self.inodesMap:
            raise FileNotFoundError
        return self.inodesMap[globalInode]

    def saveFh(self, globalFh, localFh):
        self.fhMap[globalFh] = localFh
    def getLocalByGlobalFh(self, globalFh):
        if not globalFh in self.fhMap:
            raise FileNotFoundError
        return self.fhMap[globalFh]

    @abstractmethod
    def lookup(self, inode_p, name):
        pass
    @abstractmethod
    def getattr(self, inode):
        pass
    @abstractmethod
    def setattr(self, inode, attr):
        pass
    @abstractmethod
    def readdir(self, inode, off):
        pass
    @abstractmethod
    def opendir(self, inode):
        pass
    @abstractmethod
    def open(self, inode, flags):
        pass
    @abstractmethod
    def read(self, fh, offset, length):
        pass
    @abstractmethod
    def write(self, fh, offset, buf):
        pass
    @abstractmethod
    def release(self, fh):
        pass
    @abstractmethod
    def mkdir(self, inode_p, name, mode):
        pass
    @abstractmethod
    def rmdir(self, inode_p, name):
        pass
    @abstractmethod
    def create(self, inode_parent, name, mode, flags):
        pass
    @abstractmethod
    def unlink(self, inode):
        pass
    @abstractmethod
    def rename(self, inode_p_old, name_old, inode_p_new, name_new):     
        pass
    @abstractmethod
    def statfs(self):
        pass
    @abstractmethod
    def readlink(self, inode):
        pass
    @abstractmethod
    def symlink(self, inode_p, name, target, ctx):
        pass
    @abstractmethod
    def link(self, inode, new_inode_p, new_name):
        pass
    @abstractmethod
    def mknod(self, inode_p, name, mode, rdev, ctx):
        pass
    @abstractmethod
    def access(self, inode, mode, ctx):
        pass
