
from enum import Enum
import subprocess
import os

class PackageTypes(Enum):

   CROSSHOST = 1
   HANDBRAKE = 2
   CROSSENV = 3
   AUTORECONF = 4

class SoftwarePackage:

    DONE_CONFIGURE = '.done-configure'
    DONE_BUILD = '.done-build'
    DONE_INSTALL = '.done-install'

    CMD_CONFIGURE = './configure'
    CMD_AUTHGEN = './autogen.sh'
    CMD_AUTORECONF = 'autoreconf'

    def __init__(self, dirname):
        self.dirname = dirname
        self.pkgname = os.path.basename(dirname)

    def is_locked(self, lockname):

        lock = os.path.join(self.dirname, lockname)

        if os.path.isfile(lock):
            return True

        return False

    def create_lock(self, lockname):

        lock = os.path.join(self.dirname, lockname)

        open(lock, 'a').close()

        return True

    def configure(self, pkgtype, dir_dest,
                  toolpath, toolchain, config_args = []):

        if self.is_locked(self.DONE_CONFIGURE):
            print('{0}: Already configured'.format(self.pkgname))
            return True

        env = None

        if pkgtype == PackageTypes.AUTORECONF:
            cmd = [ self.CMD_AUTORECONF, '-i']

            r = subprocess.run(cmd, check=True, cwd=self.dirname, env=env)
            if r.returncode != 0:
                raise Exception('{0}: Unable to autoreconf'.format(self.pkgname))

        if not os.path.isfile(os.path.join(self.dirname, self.CMD_CONFIGURE)):
            if os.path.isfile(os.path.join(self.dirname, self.CMD_AUTHGEN)):
                cmd = [ self.CMD_AUTHGEN ]
                r = subprocess.run(cmd, check=True, cwd=self.dirname, env=env)
                if r.returncode != 0:
                    raise Exception('{0}: Unable to autogen'.format(self.pkgname))
            else:
                raise Exception('{0}: No configure or autogen'.format(self.pkgname))

        if not os.path.isfile(os.path.join(self.dirname, self.CMD_CONFIGURE)):
            raise Exception('{0}: No configure after autogen'.format(self.pkgname))

        if pkgtype == PackageTypes.CROSSHOST or pkgtype == PackageTypes.AUTORECONF:

            cmd = [ self.CMD_CONFIGURE,
                    '--prefix={0}'.format(dir_dest),
                    '--host={0}'.format(toolchain)
            ]

            cmd += config_args

        elif pkgtype == PackageTypes.HANDBRAKE:

            cmd = [ self.CMD_CONFIGURE,
                    '--prefix={0}'.format(dir_dest),
                    '--disable-gtk',
                    '--cross={0}'.format(os.path.join(toolpath, toolchain))
            ]

            cmd += config_args

        elif pkgtype == PackageTypes.CROSSENV:

            toolprefix = os.path.join(toolpath, toolchain)

            env = {
                'CC': '{0}-gcc'.format(toolprefix),
                'CXX': '{0}-g++'.format(toolprefix),
                'AR': '{0}-ar'.format(toolprefix),
                'RANLIB': '{0}-ranlib'.format(toolprefix),
                'LD': '{0}-ld'.format(toolprefix),
                'STRIP': '{0}-strip'.format(toolprefix)
            }

            cmd = [ './configure',
                    '--prefix={0}'.format(dir_dest)
            ]

            cmd += config_args

        r = subprocess.run(cmd, check=True, cwd=self.dirname, env=env)
        if r.returncode != 0:
            raise Exception('{0}: Unable to configure'.format(self.pkgname))

        self.create_lock(self.DONE_CONFIGURE)

        return True

    def build(self, build_dir = None):

        if self.is_locked(self.DONE_BUILD):
            print('{0}: Already built'.format(self.pkgname))
            return True

        build_dir = self.dirname if build_dir is None else os.path.join(self.dirname, build_dir)

        cmd = 'make'

        r = subprocess.run(cmd, check=True, cwd=build_dir)

        if r.returncode != 0:
            raise Exception('{0}: Unable to build'.format(self.pkgname))

        self.create_lock(self.DONE_BUILD)

        return True

    def install(self, build_dir = None):

        if self.is_locked(self.DONE_INSTALL):
            print('{0}: Already installed'.format(self.pkgname))
            return True

        build_dir = self.dirname if build_dir is None else os.path.join(self.dirname, build_dir)

        cmd = ['make', 'install']

        r = subprocess.run(cmd, check=True, cwd=build_dir)

        if r.returncode != 0:
            raise Exception('{0}: Unable to install'.format(self.pkgname))

        self.create_lock(self.DONE_INSTALL)

        return True
