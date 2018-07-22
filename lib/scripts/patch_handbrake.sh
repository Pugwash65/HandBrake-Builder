#!/bin/sh

LIBVPX_DEFS=contrib/libvpx/module.defs
MAKE_DEFS=make/include/main.defs
HANDBRAKE_M4=build/project/handbrake.m4
HANDBRAKE_MAKEFILE=build/GNUmakefile

# Force correct host target to allow VPX to cross compile correctly

/bin/perl -spi -e 's/--target=x86_64-win64-gcc/--target=generic-gnu/' ${LIBVPX_DEFS}

if [ $? != 0 ]; then
 echo "Patch ${LIBVPX_DEFS} faied"
 exit 1
fi

# Force module defs to compile standard dependencies

/bin/perl -spi -e 's/(darwin\s+cygwin\s+mingw)/$1 linux/' ${MAKE_DEFS}

if [ $? != 0 ]; then
 echo "Patch ${MAKE_DEFS} faied"
 exit 1
fi

# Force NVIDIA GPU encoding to be disabled

/bin/perl -spi -e 's/^(.*<<__FEATURE_nvenc>>.*<<)\d(>>.*)$/${1}0${2}/' ${HANDBRAKE_M4}

if [ $? != 0 ]; then
 echo "Patch ${HANDBRAKE_M4} faied"
 exit 1
fi

/bin/perl -spi -e 's/^(FEATURE\.nvenc.*)\d(.*)$/${1}0${2}/' ${HANDBRAKE_MAKEFILE}

if [ $? != 0 ]; then
 echo "Patch ${HANDBRAKE_MAKEFILE} faied"
 exit 1
fi

exit 0