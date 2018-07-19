
from handbrake_builder.softwarepackage import SoftwarePackage
import os
import re
import subprocess
import sys

class HandbrakeBuilder:

    TOOLCHAIN = "x86_64-QNAP-linux-gnu"
    TOOLPATH = "/home/development/CT/{0}/cross-tools/bin".format(TOOLCHAIN)

    def __init__(self, build_base):
        self.filename = __file__
        self.build_base = build_base

        if not os.path.isdir(build_base):
            raise Exception('{0}: Project build directory is missing'.format(build_base))

        self.dir_download = os.path.join(build_base, 'download')
        self.dir_source = os.path.join(build_base, 'src')
        self.dir_handbrake = os.path.join(self.dir_source, 'HandBrake')
        self.dir_dest = os.path.join(self.dir_handbrake, 'build', 'contrib')
        self.dir_lib = os.path.join(self.dir_dest, 'lib')
        self.dir_scripts = os.path.join(os.path.dirname(sys.argv[0]), 'scripts')

        for dir in [self.dir_download, self.dir_source]:
            if not os.path.isdir(dir):
                os.mkdir(dir, 0o700)
            if not os.path.isdir(dir):
                raise Exception('{0}: Unable to create directory'.format(dir))

    def set_environment(self):

        os.environ['PKG_CONFIG_PATH'] = '{0}/lib/pkgconfig'.format(self.dir_dest)
        os.environ['PATH'] += os.pathsep + os.path.join(self.TOOLPATH)
        os.environ['PATH'] += os.pathsep + os.path.join(self.dir_dest, 'bin')
        os.environ['CFLAGS'] = '-I{0}/include -I{0}/include/libxml2 -fPIC'.format(self.dir_dest, self.dir_dest)
        # os.environ['CFLAGS'] = '-I{0}/include -I{0}/include/libxml2'.format(self.dir_dest, self.dir_dest)
        os.environ['LDFLAGS'] = '-L{0}/lib'.format(self.dir_dest)
        os.environ['LD_LIBRARY_PATH'] = self.dir_dest

        # For libvpx

        os.environ['CROSS'] = '{0}-'.format(self.TOOLCHAIN)

        return True

    def fetch_tarball(self, url):

        tarball = os.path.basename(url)
        dirname = os.path.splitext(tarball)
        dirname = os.path.splitext(dirname[0])
        dirname = os.path.join(self.dir_source, dirname[0])

        srcball = os.path.join(self.dir_download, tarball)

        package = SoftwarePackage(dirname)

        # Source directory already exists

        if os.path.isdir(dirname):
            return package

        # Package already downloaded

        if not os.path.isfile(os.path.join(self.dir_download, tarball)):

            cmd = [ '/bin/wget', '-P', self.dir_download, url ]
            r = subprocess.run(cmd, check=True)
            if r.returncode != 0:
                raise Exception('{0}: Unable to download'.format(tarball))

        cmd = [ '/bin/tar', '-C', self.dir_source,  '-xf', srcball ]
        r = subprocess.run(cmd, check=True)
        if r.returncode != 0:
            raise Exception('{0}: Unable to extract'.format(tarball))

        return package

    def fetch_git(self, url):

        dirname = os.path.splitext(os.path.basename(url))
        dirname = os.path.join(self.dir_source, dirname[0])

        package = SoftwarePackage(dirname)
        pkgname = package.pkgname

        if not os.path.isdir(dirname):
            cmd = ['/bin/git', 'clone', url, dirname]
            r = subprocess.run(cmd, check=True)
            if r.returncode != 0:
                raise Exception('{0}: Unable to clone'.format(dirname))

            return package
        else:
            cmd = ['/bin/git', '-C', dirname, 'rev-parse', 'HEAD']
            r = subprocess.run(cmd, check=True, stdout=subprocess.PIPE)
            if r.returncode != 0:
                raise Exception('{0}: Unable to check HEAD rev'.format(pkgname))
            local = r.stdout

            cmd = ['/bin/git', '-C', dirname, 'rev-parse', '@{upstream}']
            r = subprocess.run(cmd, check=True, stdout=subprocess.PIPE)
            if r.returncode != 0:
                raise Exception('{0}: Unable to check upstream rev'.format(pkgname))
            remote = r.stdout

            if local == remote:
                print('{0}: No changes to repo'.format(pkgname))
                return package

            r = subprocess.run(cmd, check=True)
            if r.returncode != 0:
                raise Exception('{0}: Unable to pull'.format(dirname))

            # Remove done flags
            return package

    def build_dep(self, url, pkgtype, **args):

        gitrepo = re.match('^.*\.git$', url)
        tarball = re.match('^.*\.tar\.gz$', url) or re.match('^.*\.tar\.bz2$', url)

        if gitrepo:
            package = self.fetch_git(url)
        elif tarball:
            package = self.fetch_tarball(url)
        else:
            raise Exception('{0}: Unknown repo type'.format(url))

        force_autogen = args['force_autogen'] if 'force_autogen' in args else []
        config_args = args['config_args'] if 'config_args' in args else []
        config_post = args['config_post'] if 'config_post' in args else []
        build_dir = args['build_dir'] if 'build_dir' in args else None
        build_args = args['build_args'] if 'build_args' in args else None
        build_flags = args['build_flags'] if 'build_flags' in args else []
        install_args = args['install_args'] if 'install_args' in args else []

        package.set_toolchain(self.TOOLPATH, self.TOOLCHAIN)
        package.configure(pkgtype, self.dir_dest, config_args, force_autogen)
        if config_post:
            package.post_configure(config_post, self.dir_scripts)

        package.build(build_dir, build_flags, build_args)
        package.install(install_args, build_dir)
