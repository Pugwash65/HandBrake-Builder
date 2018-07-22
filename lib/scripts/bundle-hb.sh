#!/bin/sh

BINARY=HandBrakeCLI
CONTRIBLIB=contrib/lib

if [ ! -f ${BINARY} ]; then
   echo "${BINARY}: Not found"
   exit 1
fi

VERSION=`./${BINARY} --version 2>/dev/null | /bin/head -1 | /bin/awk '{print $2}' | /bin/sed -e 's/-master//'`

if [ "x${VERSION}" = "x" ]; then
   echo "Unable to determine version number"
   exit 1
fi

BUNDLEBASE=`pwd`
BUNDLEBASE=`/bin/realpath ${BUNDLEBASE}`
BUNDLEBASE=`/bin/dirname ${BUNDLEBASE}`
BUNDLEBASE=`/bin/dirname ${BUNDLEBASE}`
BUNDLEBASE=`/bin/dirname ${BUNDLEBASE}`
BUNDLEBASE=${BUNDLEBASE}/bundle

BUNDLENAME=${VERSION}
BUNDLEDIR=${BUNDLEBASE}/${BUNDLENAME}

TARBALL=${BUNDLEBASE}/handbrake-${VERSION}.tar.gz

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

/bin/tar -C ${BUNDLEBASE} -czf ${TARBALL} ${BUNDLENAME}
if [ $? != 0 ]; then
   echo "Failed to tar bundle"
   exit 1
fi

rm -rf ${BUNDLEDIR}
if [ $? != 0 ]; then
   echo "Failed to cleanup temporary bundle directory"
   exit 1
fi

exit 0