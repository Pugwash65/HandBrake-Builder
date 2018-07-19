#!/bin/sh

LIBVPX_DEFS=contrib/libvpx/module.defs
MAKE_DEFS=make/include/main.defs

/bin/perl -spi -e 's/--target=x86_64-win64-gcc/--target=generic-gnu/' ${LIBVPX_DEFS}

if [ $? != 0 ]; then
 echo "Patch ${LIBVPX_DEFS} faied"
 exit 1
fi

/bin/perl -spi -e 's/(darwin\s+cygwin\s+mingw)/$1 linux/' ${MAKE_DEFS}

if [ $? != 0 ]; then
 echo "Patch ${MAKE_DEFS} faied"
 exit 1
fi

exit 0