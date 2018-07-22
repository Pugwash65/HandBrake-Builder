
from enum import Enum
import subprocess
import time
import sys
import os

class PackageTypes(Enum):

   CROSSHOST = 1
   HANDBRAKE = 2
   CROSSENV = 3
   AUTORECONF = 4
   LIBEXPAT = 5
   PLAINENV = 6

class BuildFlags(Enum):

    SETENV = 1

class SoftwarePackage:

    DONE_CONFIGURE = '.done-configure'
    DONE_BUILD = '.done-build'
    DONE_INSTALL = '.done-install'
    DONE_SCRIPT = '.done-script'

    CMD_CONFIGURE = './configure'
    CMD_AUTHGEN = './autogen.sh'
    CMD_AUTORECONF = 'autoreconf'

    NOTIFY_DELAY = 0

    def __init__(self, dirname):
        self.toolpath = None
        self.toolchain = None

        self.dirname = dirname
        self.pkgname = os.path.basename(dirname)
        self.env = {
            'PATH': os.environ['PATH'],
            'CFLAGS': os.environ['CFLAGS'],
            'LDFLAGS': os.environ['LDFLAGS'],
            'PKG_CONFIG_PATH': os.environ['PKG_CONFIG_PATH']
        }

    @staticmethod
    def notify(msg):

        print(msg)
        time.sleep(SoftwarePackage.NOTIFY_DELAY)

        return True

    def set_toolchain(self, toolpath, toolchain):
        self.toolpath = toolpath
        self.toolchain = toolchain

        return True

    def extend_env(self, toolpath, toolchain):

        toolprefix = os.path.join(toolpath, toolchain)

        env = self.env
        env['CC'] = '{0}-gcc'.format(toolprefix)
        env['CXX'] = '{0}-g++'.format(toolprefix)
        env['AR'] = '{0}-ar'.format(toolprefix)
        env['RANLIB'] = '{0}-ranlib'.format(toolprefix)
        env['LD'] = '{0}-ld'.format(toolprefix)
        env['STRIP'] = '{0}-strip'.format(toolprefix)

        return env

    def is_locked(self, lockname):

        lock = os.path.join(self.dirname, lockname)

        if os.path.isfile(lock):
            return True

        return False

    def create_lock(self, lockname):

        lock = os.path.join(self.dirname, lockname)

        open(lock, 'a').close()

        return True

    def configure(self, pkgtype, dir_dest, config_args=[], force_autogen=False):

        toolpath = self.toolpath
        toolchain = self.toolchain

        if self.is_locked(self.DONE_CONFIGURE):
            self.notify('=== Already configured: {0} ==='.format(self.pkgname))
            return True

        if pkgtype == PackageTypes.PLAINENV:
            self.create_lock(self.DONE_CONFIGURE)
            return True

        env = self.env

        dirname = self.dirname

        if pkgtype == PackageTypes.AUTORECONF:
            cmd = [ self.CMD_AUTORECONF, '-i']

            r = subprocess.run(cmd, check=True, cwd=dirname, env=env)
            if r.returncode != 0:
                raise Exception('{0}: Unable to autoreconf'.format(self.pkgname))

        elif pkgtype == PackageTypes.LIBEXPAT:
            cmd = [ './buildconf.sh']
            dirname = os.path.join(dirname, 'expat')

            r = subprocess.run(cmd, check=True, cwd=dirname, env=env)
            if r.returncode != 0:
                raise Exception('{0}: Unable to buildconf'.format(self.pkgname))

        if force_autogen or not os.path.isfile(os.path.join(dirname, self.CMD_CONFIGURE)):
            if os.path.isfile(os.path.join(dirname, self.CMD_AUTHGEN)):
                cmd = [ self.CMD_AUTHGEN ]
                r = subprocess.run(cmd, check=True, cwd=dirname, env=env)
                if r.returncode != 0:
                    raise Exception('{0}: Unable to autogen'.format(self.pkgname))
            # else:
            #     raise Exception('{0}: No configure or autogen'.format(self.pkgname))
        #
        # if not os.path.isfile(os.path.join(dirname, self.CMD_CONFIGURE)):
        #     raise Exception('{0}: No configure after autogen'.format(self.pkgname))

        if pkgtype == PackageTypes.CROSSHOST or pkgtype == PackageTypes.AUTORECONF or \
           pkgtype == PackageTypes.LIBEXPAT:

            cmd = [ self.CMD_CONFIGURE,
                    '--prefix={0}'.format(dir_dest),
                    '--host={0}'.format(toolchain)
            ]

            cmd += config_args

        elif pkgtype == PackageTypes.HANDBRAKE:

            cmd = [ self.CMD_CONFIGURE,
                    '--prefix={0}'.format(dir_dest),
                    '--disable-gtk',
                    '--force',
                    '--cross={0}'.format(os.path.join(toolpath, toolchain))
            ]

            cmd += config_args

        elif pkgtype == PackageTypes.CROSSENV:

            env = self.extend_env(toolpath, toolchain)

            cmd = [ './configure',
                    '--prefix={0}'.format(dir_dest)
            ]

            cmd += config_args

        self.notify('=== CONFIGURE: {0} ==='.format(self.pkgname))
        sys.stdout.flush()

        r = subprocess.run(cmd, check=True, cwd=dirname, env=env)

        if r.returncode != 0:
            raise Exception('{0}: Unable to configure'.format(self.pkgname))

        self.create_lock(self.DONE_CONFIGURE)

        return True

    def script(self, scripts, dir_scripts, build_dir = None):

        build_dir = self.dirname if build_dir is None else os.path.join(self.dirname, build_dir)

        for script in scripts:
            lockname = '{0}-{1}'.format(self.DONE_SCRIPT, os.path.splitext(script)[0])

            if self.is_locked(lockname):
                self.notify('=== Already run script: {0} ==='.format(script))
                return True

            script = os.path.join(dir_scripts, script)
            if not os.path.isfile(script):
                raise Exception('{0}: Script not found'.format(script))

            self.notify('=== SCRIPT: {0} ==='.format(script))
            sys.stdout.flush()

            r = subprocess.run(script, check=True, cwd=build_dir)

            if r.returncode != 0:
                raise Exception('{0}: Unable to execute script'.format(script))

            self.create_lock(lockname)

        return True

    def build(self, build_dir = None, build_flags = [], build_args = []):

        if self.is_locked(self.DONE_BUILD):
            self.notify('=== Already built: {0} ==='.format(self.pkgname))
            return True

        if BuildFlags.SETENV in build_flags:
            env = self.extend_env(self.toolpath, self.toolchain)
        else:
            env = []

        build_dir = self.dirname if build_dir is None else os.path.join(self.dirname, build_dir)

        # cmd = ['make', build_dir]
        cmd = ['make']

        for key in env:
            cmd += ['{0}={1}'.format(key, env[key])]

        self.notify('=== BUILD: {0} ==='.format(self.pkgname))
        sys.stdout.flush()

        r = subprocess.run(cmd, check=True, cwd=build_dir)

        if r.returncode != 0:
            raise Exception('{0}: Unable to build'.format(self.pkgname))

        self.create_lock(self.DONE_BUILD)

        return True

    def install(self, install_args = [], build_dir = None):

        if self.is_locked(self.DONE_INSTALL):
            self.notify('=== Already installed: {0} ==='.format(self.pkgname))
            return True

        install_args = install_args if install_args else ['install']

        build_dir = self.dirname if build_dir is None else os.path.join(self.dirname, build_dir)

        cmd = ['make']
        cmd += install_args

        self.notify('=== INSTALL: {0} ==='.format(self.pkgname))
        sys.stdout.flush()

        r = subprocess.run(cmd, check=True, cwd=build_dir)

        if r.returncode != 0:
            raise Exception('{0}: Unable to install'.format(self.pkgname))

        self.create_lock(self.DONE_INSTALL)

        return True
