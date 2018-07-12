
from handbrake_builder import HandbrakeBuilder

import argparse
import sys

try:
    parser = argparse.ArgumentParser(description='Build HandBrakeCLI')
    parser.add_argument('--build-dir', action='store', help='set the build directory')


    args = parser.parse_args()
    build_dir = args.build_dir

    builder = HandbrakeBuilder(build_dir)
    builder.set_environment()
    builder.build_dep('https://github.com/HandBrake/HandBrake.git')

    sys.exit(0)
except Exception as e:

    print(e)
    sys.exit(1)