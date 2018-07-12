
import os


class HandbrakeBuilder:

    TOOLCHAIN = "x86_64-QNAP-linux-gnu"
    TOOLPATH = "/home/development/CT/{0}/cross-tools/bin".format(TOOLCHAIN)

    def __init__(self, build_base):
        self.filename = __file__
        self.build_base = build_base

        if not os.path.isdir(build_base):
            raise Exception('{0}: Build directory is missing'.format(build_base))

        self.dir_download = os.path.join(build_base, 'download')
        self.dir_source = os.path.join(build_base, 'src')
        self.dir_handbrake = os.path.join(self.dir_source, 'HandBrake')
        self.dir_dest = os.path.join(self.dir_handbrake, 'build', 'contrib')

        for dir in [self.dir_download, self.dir_source]:
            if not os.path.isdir(dir):
                os.mkdir(dir, 0o700)
            if not os.path.isdir(dir):
                raise Exception('{0}: Unable to create directory'.format(dir))

    def set_environment(self):

        os.environ['PKG_CONFIG_PATH'] = '{0}/lib/pkgconfig'.format(self.dir_dest)
        os.environ['PATH'] += os.pathsep + os.path.join(self.TOOLPATH, 'bin')
        os.environ['PATH'] += os.pathsep + os.path.join(self.dir_dest, 'bin')

        # export
        # PATH =${TOOLPATH}: / bin: / usr / bin:${BUILD_DIR} / bin
        # export
        # CFLAGS = "-I${BUILD_DIR}/include -I${BUILD_DIR}/include/libxml2"
        # export
        # LDFLAGS = -L${BUILD_DIR} / lib
