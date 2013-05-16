#!/bin/bash

INSTALL_DIR=deb/usr/share/useraid

mkdir -p $INSTALL_DIR
cp ../*.py $INSTALL_DIR

fakeroot dpkg-deb --build deb

mv deb.deb useraid-1.0.deb
