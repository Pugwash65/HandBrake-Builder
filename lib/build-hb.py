
from handbrake_builder import HandbrakeBuilder
from handbrake_builder.softwarepackage import PackageTypes
import argparse
import sys

try:
    parser = argparse.ArgumentParser(description='Build HandBrakeCLI')
    parser.add_argument('--build-dir', action='store', help='set the build directory')


    args = parser.parse_args()
    build_dir = args.build_dir

    builder = HandbrakeBuilder(build_dir)
    builder.set_environment()
    hb = builder.fetch_git('https://github.com/HandBrake/HandBrake.git')
    # hb.configure(PackageTypes.HANDBRAKE, hb.dirname, builder.TOOLPATH, builder.TOOLCHAIN)

    builder.build_dep('https://datapacket.dl.sourceforge.net/project/lame/lame/3.100/lame-3.100.tar.gz', PackageTypes.CROSSHOST)
    builder.build_dep('https://archive.mozilla.org/pub/opus/opus-1.2.1.tar.gz', PackageTypes.CROSSHOST)
    builder.build_dep('http://downloads.us.xiph.org/releases/speex/speex-1.2.0.tar.gz', PackageTypes.CROSSHOST)
    builder.build_dep('https://github.com/madler/zlib.git', PackageTypes.CROSSENV)
    builder.build_dep('https://git.tukaani.org/xz.git', PackageTypes.CROSSHOST)
    builder.build_dep('http://xmlsoft.org/sources/libxml2-2.9.8.tar.gz', PackageTypes.CROSSHOST, config_args = ['--without-python'])
    builder.build_dep('https://github.com/akheron/jansson.git', PackageTypes.AUTORECONF)
    builder.build_dep('https://github.com/xiph/ogg.git', PackageTypes.CROSSHOST)
    builder.build_dep('http://downloads.xiph.org/releases/vorbis/libvorbis-1.3.6.tar.gz', PackageTypes.CROSSHOST)
    builder.build_dep('https://github.com/erikd/libsamplerate.git', PackageTypes.CROSSHOST)
    builder.build_dep('http://git.videolan.org/git/x264.git', PackageTypes.CROSSHOST)
    ## fix config.mak --host not work on configure
    ## make install-lib-dev
    ## make install-lib-shared

    hb.build('build')

# https://archive.mozilla.org/pub/opus/opus-1.2.1.tar.gz crosshost
# http://downloads.us.xiph.org/releases/speex/speex-1.2.0.tar.gz crossho
#st
# http://xmlsoft.org/sources/libxml2-2.9.8.tar.gz crosshost --without-py
#thon
#host
# git://git.sv.nongnu.org/freetype/freetype2.git crosshost
# https://github.com/fribidi/fribidi.git crosshost
# https://github.com/libass/libass.git crosshost --disable-require-syste
#m-font-provider
# https://git.xiph.org/theora.git crosshost
# https://github.com/libexpat/libexpat/releases/download/R_2_2_5/expat-2
#.2.5.tar.bz2 crosshost
# https://www.freedesktop.org/software/fontconfig/release/fontconfig-2.1
#3.0.tar.bz2 crosshost
# https://github.com/harfbuzz/harfbuzz.git crosshost
# https://github.com/enthought/bzip2-1.0.6.git plainenv


    sys.exit(0)
except Exception as e:

    print(e)
    sys.exit(1)