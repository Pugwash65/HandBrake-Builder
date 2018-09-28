
from handbrake_builder import HandbrakeBuilder
from handbrake_builder.softwarepackage import PackageTypes, BuildFlags
import argparse
import sys

try:
    parser = argparse.ArgumentParser(description='Build HandBrakeCLI')
    parser.add_argument('--build-dir', action='store', help='set the build directory')
    parser.add_argument('--toolchain-path', action='store', help='set the root directory of the toolchain')

    args = parser.parse_args()
    build_dir = args.build_dir
    toolchain_path = args.toolchain_path

    builder = HandbrakeBuilder(build_dir, toolchain_path)
    builder.set_environment()

    build_deps = [
        {
          'url': 'https://datapacket.dl.sourceforge.net/project/lame/lame/3.100/lame-3.100.tar.gz',
          'pkgtype': PackageTypes.CROSSHOST
        },
        {
          'url' : 'https://archive.mozilla.org/pub/opus/opus-1.2.1.tar.gz',
          'pkgtype': PackageTypes.CROSSHOST
        },
        {
          'url' : 'http://downloads.us.xiph.org/releases/speex/speex-1.2.0.tar.gz',
          'pkgtype' : PackageTypes.CROSSHOST
        },
        {
          'url': 'https://github.com/madler/zlib.git',
          'pkgtype': PackageTypes.CROSSENV,
          'install_args': ['install', 'prefix={0}'.format(builder.dir_dest)]
        },
        {
          'url': 'https://git.tukaani.org/xz.git',
          'pkgtype': PackageTypes.CROSSHOST
        },
        {
          'url': 'http://xmlsoft.org/sources/libxml2-2.9.8.tar.gz',
          'pkgtype': PackageTypes.CROSSHOST,
          'config_args': ['--without-python','--without-lzma']
        },
        # {
        #   'url': 'https://github.com/akheron/jansson.git',
        #   'pkgtype': PackageTypes.AUTORECONF
        # },
        # {
        #   'url': 'https://github.com/xiph/ogg.git',
        #   'pkgtype': PackageTypes.CROSSHOST
        # },
        # {
        #   'url': 'http://downloads.xiph.org/releases/vorbis/libvorbis-1.3.6.tar.gz',
        #   'pkgtype': PackageTypes.CROSSHOST
        # },
        # {
        #   'url': 'https://github.com/erikd/libsamplerate.git',
        #   'pkgtype': PackageTypes.CROSSHOST
        # },
        {
          'url': 'git://git.sv.nongnu.org/freetype/freetype2.git',
          'pkgtype': PackageTypes.CROSSHOST,
          'force_autogen': True
        },
        # {
        #   'url': 'https://github.com/fribidi/fribidi.git',
        #   'pkgtype': PackageTypes.CROSSHOST
        # },
        # {
        #   'url': 'https://github.com/libass/libass.git',
        #   'pkgtype': PackageTypes.CROSSHOST,
        #   'config_args': ['--disable-require-system-font-provider']
        # },
        # {
        #   'url': 'http://git.videolan.org/git/x264.git',
        #   'pkgtype': PackageTypes.CROSSHOST,
        #   'config_args': ['--enable-shared'],
        #   'config_post': ['patch_x264.sh'],
        #   'build_args': [],
        #   'install_args': []
        # },
        # {
        #   'url': 'http://git.videolan.org/git/x264.git',
        #   'pkgtype': PackageTypes.CROSSHOST,
        #   'config_args': ['--enable-shared'],
        #   'config_post': ['patch_x264.sh'],
        #   'build_args': ['lib-shared', 'SONAME=libx264.so'],
        #   'install_args': ['install-lib-dev', 'install-lib-shared']
        # },
        {
          'url': 'https://github.com/libexpat/libexpat.git',
          'pkgtype': PackageTypes.LIBEXPAT,
          'config_args': ['--without-xmlwf'],
          'build_dir': 'expat'
        },
        # {
        #   'url': 'https://git.xiph.org/theora.git',
        #   'pkgtype': PackageTypes.CROSSHOST,
        #   'config_args': ['--with-ogg={0}'.format(builder.dir_dest)]
        # },
        # {
        #   'url': 'https://github.com/harfbuzz/harfbuzz.git',
        #   'pkgtype': PackageTypes.CROSSHOST
        # },
        {
          'url': 'https://vorboss.dl.sourceforge.net/project/libuuid/libuuid-1.0.3.tar.gz',
          'pkgtype': PackageTypes.CROSSHOST
        },
        {
          'url': 'http://ftp.gnu.org/pub/gnu/gperf/gperf-3.1.tar.gz',
          'pkgtype': PackageTypes.CROSSHOST
        },
        {
          'url': 'https://www.freedesktop.org/software/fontconfig/release/fontconfig-2.13.0.tar.bz2',
          'pkgtype': PackageTypes.CROSSHOST
        },
        {
          'url': 'https://github.com/enthought/bzip2-1.0.6.git',
          'pkgtype': PackageTypes.PLAINENV,
          'build_flags': [BuildFlags.SETENV],
          'install_args': ['install', 'PREFIX={0}'.format(builder.dir_dest)]
        }
    ]

    hb = builder.fetch_git('https://github.com/HandBrake/HandBrake.git')

    hb.set_toolchain(builder.toolchain_path, builder.TOOLCHAIN)

    hb.configure(PackageTypes.HANDBRAKE, hb.dirname, builder.toolchain_path, builder.TOOLCHAIN)
    hb.script(['patch_handbrake.sh'], builder.dir_scripts)

    for dep_data in build_deps:
        builder.build_dep(dep_data)

    hb.build('build')
    hb.script(['bundle-hb.sh'], builder.dir_scripts, 'build')

    sys.exit(0)

    # builder.build_dep('https://datapacket.dl.sourceforge.net/project/lame/lame/3.100/lame-3.100.tar.gz', PackageTypes.CROSSHOST)
    # builder.build_dep('https://archive.mozilla.org/pub/opus/opus-1.2.1.tar.gz', PackageTypes.CROSSHOST)
    # builder.build_dep('http://downloads.us.xiph.org/releases/speex/speex-1.2.0.tar.gz', PackageTypes.CROSSHOST)
    # builder.build_dep('https://github.com/madler/zlib.git', PackageTypes.CROSSENV,
    #                   install_args=['install', 'prefix={0}'.format(builder.dir_dest)])
    # builder.build_dep('https://git.tukaani.org/xz.git', PackageTypes.CROSSHOST)
    # builder.build_dep('http://xmlsoft.org/sources/libxml2-2.9.8.tar.gz', PackageTypes.CROSSHOST, config_args = ['--without-python','--without-lzma'])
    # # builder.build_dep('https://github.com/akheron/jansson.git', PackageTypes.AUTORECONF)
    # # builder.build_dep('https://github.com/xiph/ogg.git', PackageTypes.CROSSHOST)
    # # builder.build_dep('http://downloads.xiph.org/releases/vorbis/libvorbis-1.3.6.tar.gz', PackageTypes.CROSSHOST)
    # # builder.build_dep('https://github.com/erikd/libsamplerate.git', PackageTypes.CROSSHOST)
    # builder.build_dep('git://git.sv.nongnu.org/freetype/freetype2.git', PackageTypes.CROSSHOST,
    #                   force_autogen=True)
    # # builder.build_dep('https://github.com/fribidi/fribidi.git', PackageTypes.CROSSHOST)
    # # builder.build_dep('https://github.com/libass/libass.git', PackageTypes.CROSSHOST,
    # #                   config_args = ['--disable-require-system-font-provider'])
    # # builder.build_dep('http://git.videolan.org/git/x264.git', PackageTypes.CROSSHOST,
    # #                   config_args=['--enable-shared'], config_post = ['patch_x264.sh'], build_args = [], install_args = [])
    # # config_args=['--enable-shared'], config_post = ['patch_x264.sh'], build_args = ['lib-shared', 'SONAME=libx264.so'], install_args = ['install-lib-dev', 'install-lib-shared'])
    # builder.build_dep('https://github.com/libexpat/libexpat.git', PackageTypes.LIBEXPAT,
    #                   config_args=['--without-xmlwf'], build_dir='expat')
    # # builder.build_dep('https://git.xiph.org/theora.git', PackageTypes.CROSSHOST,
    # #                   config_args=['--with-ogg={0}'.format(builder.dir_dest)])
    # # builder.build_dep('https://github.com/harfbuzz/harfbuzz.git', PackageTypes.CROSSHOST)
    # builder.build_dep('https://vorboss.dl.sourceforge.net/project/libuuid/libuuid-1.0.3.tar.gz', PackageTypes.CROSSHOST)
    # builder.build_dep('http://ftp.gnu.org/pub/gnu/gperf/gperf-3.1.tar.gz', PackageTypes.CROSSHOST)
    # builder.build_dep('https://www.freedesktop.org/software/fontconfig/release/fontconfig-2.13.0.tar.bz2', PackageTypes.CROSSHOST)
    # builder.build_dep('https://github.com/enthought/bzip2-1.0.6.git', PackageTypes.PLAINENV,
    #                   build_flags=[BuildFlags.SETENV], install_args=['install', 'PREFIX={0}'.format(builder.dir_dest)])

except Exception as e:

    print(e)
    sys.exit(1)