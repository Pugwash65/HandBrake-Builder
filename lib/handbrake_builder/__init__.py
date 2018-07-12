
import os
import re
import subprocess

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

        return True
        # export
        # PATH =${TOOLPATH}: / bin: / usr / bin:${BUILD_DIR} / bin
        # export
        # CFLAGS = "-I${BUILD_DIR}/include -I${BUILD_DIR}/include/libxml2"
        # export
        # LDFLAGS = -L${BUILD_DIR} / lib

    def fetch_git(self, url):

        dirname = os.path.splitext(os.path.basename(url))
        dirname = os.path.join(self.dir_source, dirname[0])

        if not os.path.isdir(dirname):
            cmd = '/bin/git clone {0} {1}'.format(url, dirname)
            r = subprocess.run(cmd, check=True)
            if r.returncode != 0:
                raise Exception('{0}: Unable to clone'.format(dirname))

            return True
        else:
            cmd = ['/bin/git', '-C', dirname, 'rev-parse', 'HEAD']
            r = subprocess.run(cmd, check=True, stdout=subprocess.PIPE)
            if r.returncode != 0:
                raise Exception('{0}: Unable to check HEAD rev'.format(dirname))
            local = r.stdout

            cmd = ['/bin/git', '-C', dirname, 'rev-parse', '@{upstream}']
            r = subprocess.run(cmd, check=True, stdout=subprocess.PIPE)
            if r.returncode != 0:
                raise Exception('{0}: Unable to check upstream rev'.format(dirname))
            remote = r.stdout

            if local == remote:
                print('{0}: No changes to repo'.format(dirname))
                return True

            r = subprocess.run(cmd, check=True)
            if r.returncode != 0:
                raise Exception('{0}: Unable to pull'.format(dirname))

            # Remove done flags
            return True

    def build_dep(self, url):

        gitrepo = re.match('^.*\.git$', url)
        tarball = re.match('^.*\.tar\.gz$', url)

        if gitrepo:
            self.fetch_git(url)
        elif tarball:
            self.fetch_tarball(url)
        else:
            raise Exception('{0}: Unknown dependency type'.format(url))

