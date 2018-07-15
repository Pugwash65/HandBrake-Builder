#!/bin/sh

TOOLCHAIN=x86_64-QNAP-linux-gnu

PATCHES="CC LD AR RANLIB"

CONFIG_MAK=config.mak

if [ ! -f ${CONFIG_MAK} ]; then
   echo "${CONFIG_MAK} not found"
   exit 1
fi


for patch in ${PATCHES}; do
  echo "Patching: $patch"

  /bin/perl -spi -e "s/^(${patch})=(.*)$/\$1=${TOOLCHAIN}-\$2/" ${CONFIG_MAK}
  if [ $? != 0 ]; then
     echo "Patch ${patch} faied"
     exit 1
  fi
done

exit 0