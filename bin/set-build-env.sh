#!/bin/sh

DEST=/home/development/n-build/src/HandBrake/build/contrib

export PATH=/home/development/CT/x86_64-QNAP-linux-gnu/cross-tools/bin:/bin:/usr/bin:${DEST}/bin

export LD_LIBRARY_PATH=${DEST}/lib

export LDFLAGS=-L${DEST}/lib

export CFLAGS="-O2 -I${DEST}/include"

export PKG_CONFIG_PATH=${DEST}/lib/pkgconfig

  # For libpvx

export CROSS=x86_64-QNAP-linux-gnu-
