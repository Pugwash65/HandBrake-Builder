
from handbrake_builder import HandbrakeBuilder
from handbrake_builder.softwarepackage import PackageTypes, BuildFlags
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

    hb.set_toolchain(builder.TOOLPATH, builder.TOOLCHAIN)

    hb.configure(PackageTypes.HANDBRAKE, hb.dirname, builder.TOOLPATH, builder.TOOLCHAIN)
    hb.script(['patch_handbrake.sh'], builder.dir_scripts)
    builder.build_dep('https://datapacket.dl.sourceforge.net/project/lame/lame/3.100/lame-3.100.tar.gz', PackageTypes.CROSSHOST)
    builder.build_dep('https://archive.mozilla.org/pub/opus/opus-1.2.1.tar.gz', PackageTypes.CROSSHOST)
    builder.build_dep('http://downloads.us.xiph.org/releases/speex/speex-1.2.0.tar.gz', PackageTypes.CROSSHOST)
    builder.build_dep('https://github.com/madler/zlib.git', PackageTypes.CROSSENV,
                      install_args=['install', 'prefix={0}'.format(builder.dir_dest)])
    builder.build_dep('https://git.tukaani.org/xz.git', PackageTypes.CROSSHOST)
    builder.build_dep('http://xmlsoft.org/sources/libxml2-2.9.8.tar.gz', PackageTypes.CROSSHOST, config_args = ['--without-python','--without-lzma'])
    # builder.build_dep('https://github.com/akheron/jansson.git', PackageTypes.AUTORECONF)
    # builder.build_dep('https://github.com/xiph/ogg.git', PackageTypes.CROSSHOST)
    # builder.build_dep('http://downloads.xiph.org/releases/vorbis/libvorbis-1.3.6.tar.gz', PackageTypes.CROSSHOST)
    # builder.build_dep('https://github.com/erikd/libsamplerate.git', PackageTypes.CROSSHOST)
    builder.build_dep('git://git.sv.nongnu.org/freetype/freetype2.git', PackageTypes.CROSSHOST,
                      force_autogen=True)
    # builder.build_dep('https://github.com/fribidi/fribidi.git', PackageTypes.CROSSHOST)
    # builder.build_dep('https://github.com/libass/libass.git', PackageTypes.CROSSHOST,
    #                   config_args = ['--disable-require-system-font-provider'])
    # builder.build_dep('http://git.videolan.org/git/x264.git', PackageTypes.CROSSHOST,
    #                   config_args=['--enable-shared'], config_post = ['patch_x264.sh'], build_args = [], install_args = [])
    # config_args=['--enable-shared'], config_post = ['patch_x264.sh'], build_args = ['lib-shared', 'SONAME=libx264.so'], install_args = ['install-lib-dev', 'install-lib-shared'])
    builder.build_dep('https://github.com/libexpat/libexpat.git', PackageTypes.LIBEXPAT,
                      config_args=['--without-xmlwf'], build_dir='expat')
    # builder.build_dep('https://git.xiph.org/theora.git', PackageTypes.CROSSHOST,
    #                   config_args=['--with-ogg={0}'.format(builder.dir_dest)])
    # builder.build_dep('https://github.com/harfbuzz/harfbuzz.git', PackageTypes.CROSSHOST)
    builder.build_dep('https://vorboss.dl.sourceforge.net/project/libuuid/libuuid-1.0.3.tar.gz', PackageTypes.CROSSHOST)
    builder.build_dep('http://ftp.gnu.org/pub/gnu/gperf/gperf-3.1.tar.gz', PackageTypes.CROSSHOST)
    builder.build_dep('https://www.freedesktop.org/software/fontconfig/release/fontconfig-2.13.0.tar.bz2', PackageTypes.CROSSHOST)
    builder.build_dep('https://github.com/enthought/bzip2-1.0.6.git', PackageTypes.PLAINENV,
                      build_flags=[BuildFlags.SETENV], install_args=['install', 'PREFIX={0}'.format(builder.dir_dest)])

    hb.build('build')
    # hb.bundle('bundle-hb.sh', builder.dir_scripts, 'build')
    hb.script(['bundle-hb.sh'], builder.dir_scripts, 'build')

    sys.exit(0)
except Exception as e:

    print(e)
    sys.exit(1)