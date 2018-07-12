#!/bin/sh

BUILD_DIR=/home/development/n-builder

local_dir=$(dirname $(dirname $(readlink -e $0)))
local_lib=${local_dir}/lib

export PYTHONPATH=${PYTHONPATH:+$PYTHONPATH:}${local_lib}

${local_dir}/venv/bin/python ${local_lib}/build-hb.py --build-dir=${BUILD_DIR} $*

exit $?

