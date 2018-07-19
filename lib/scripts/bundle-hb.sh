#!/bin/sh

BINARY=HandBrakeCLI
CONTRIBLIB=contrib/lib

if [ ! -f ${BINARY} ]; then
   echo "${BINARY}: Not found"
   exit 1
fi

BUNDLEDIR=`pwd`
BUNDLEDIR=`/bin/realpath ${BUNDLEDIR}`
BUNDLEDIR=`/bin/dirname ${BUNDLEDIR}`
BUNDLEDIR=`/bin/dirname ${BUNDLEDIR}`
BUNDLEDIR=`/bin/dirname ${BUNDLEDIR}`
BUNDLEDIR=${BUNDLEDIR}/bundle

BINDIR=${BUNDLEDIR}/bin
LIBDIR=${BUNDLEDIR}/lib

[ -f ${BUNDLEDIR} ] && /bin/rm -rf ${BUNDLEDIR}

/bin/mkdir -p ${BINDIR}
/bin/mkdir -p ${LIBDIR}

/bin/cp ${BINARY} ${BINDIR}

libs=`/bin/ldd ${BINARY} | /bin/awk '{print $1}'`

for lib in ${libs}; do
  l="${lib%.*}"
  l="${l%.*}"

  files=`/bin/ls ${CONTRIBLIB}/$l* 2>/dev/null`

  [ "x${files}" = "x" ] && continue

  for f in ${files}; do
    cp ${f} ${LIBDIR}
  done
done
