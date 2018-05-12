import subprocess
import sys
import os


def check_project_structure(modules, packages, dirs):
    root = os.path.dirname(os.path.abspath(__file__))

    for dir in dirs:
        path = os.path.join(root, dir)
        if not os.path.exists(path) or not os.path.isdir(path):
            sys.stderr.write('directory: {} is invalid!\n'.format(dir))
            sys.exit(2)

    for package in packages:
        path = os.path.join(root, package)
        if not os.path.exists(path) or not os.path.isdir(path) or not os.path.exists(os.path.join(path, '__init__.py')):
            sys.stderr.write('package: {} is invalid!\n'.format(dir))
            sys.exit(3)

    for module in modules:
        path = os.path.join(root, module)
        if not os.path.exists(path) or not os.path.isfile(path):
            sys.stderr.write('module: {} is invalid!\n'.format(module))
            sys.exit(4)

    sys.stdout.write('project...OK\n')


def parse_dependencies():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dependencies.txt')
    if not os.path.exists(path):
        sys.stderr.write('Missing dependencies.txt!')
        sys.exit(1)

    dependencies = []
    with open(path, 'r') as f:
        line = f.readline()
        while line:
            if '#' in line:  # remove comments
                line = line.split('#')[0]

            line = line.strip().split(':')
            dependencies.append((line[0], line[1]))

            line = f.readline()

    return dependencies


def exec_pip(dependency):
    command = ''
    if dependency[1] == '-1':
        command = ['python', '-m', 'pip', 'install', dependency[0]]
    else:
        command = ['python', '-m', 'pip', 'install', dependency[0] + dependency[1]]

    try:
        subprocess.check_call(command, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        sys.stdout.write(dependency[0] + '...OK\n')
    except subprocess.CalledProcessError as e:
        sys.stderr.write(str(e) + '\n' + dependency[0] + '...BAD\n')


title = 'Python 3 Project template'
description = 'A project template for python 3'
author = 'Dylan David Randall'
author_email = 'dylan.d.randall@gmail.com'
version = '0.0.0'
download_url = ''

dirs = ['logs']
packages = ['injection', 'logger']
modules = ['definitions.py', 'dependencies.txt']

sys.stdout.write('checking project structure...\n')
check_project_structure(modules, packages, dirs)

sys.stdout.write('\nsetting up dependencies...\n')
for dependency in parse_dependencies():
    exec_pip(dependency)

sys.stdout.write('\nquick setup finished\n')
