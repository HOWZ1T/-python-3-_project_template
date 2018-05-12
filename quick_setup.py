import subprocess
import sys
import os


def check_project_structure(modules, packages, dirs):
    root = os.path.dirname(os.path.abspath(__file__))

    for dir in dirs:
        path = os.path.join(root, dir)
        if not os.path.exists(path) or not os.path.isdir(path):
            sys.stderr.write('directory: {} is missing / invalid!\n'.format(dir))
            sys.exit(2)

    for package in packages:
        path = os.path.join(root, package)
        if not os.path.exists(path) or not os.path.isdir(path) or not os.path.exists(os.path.join(path, '__init__.py')):
            sys.stderr.write('package: {} is missing / invalid!\n'.format(dir))
            sys.exit(3)

    for module in modules:
        path = os.path.join(root, module)
        if not os.path.exists(path) or not os.path.isfile(path):
            sys.stderr.write('module: {} is missing / invalid!\n'.format(module))
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
            hashtag_index = -1
            for i in range(0, len(line)):
                if line[i] == '#':
                    hashtag_index = i
                    break

            if hashtag_index >= 0:
                line = line[:hashtag_index]

            if len(line) > 0:
                if line[0] != '#':
                    line = line.strip()
                    dependencies.append(line)

            line = f.readline()

    return dependencies


def exec_pip(dependency):
    command = ['python', '-m', 'pip', 'install', dependency]

    try:
        subprocess.check_call(command, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        sys.stdout.write(dependency + '...OK\n')
    except subprocess.CalledProcessError as e:
        sys.stderr.write(str(e) + '\n' + dependency + '...BAD\n')


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

dependencies = parse_dependencies()
if len(dependencies) > 0:
    sys.stdout.write('\nsetting up dependencies... (this may take some time)\n')
    for dependency in dependencies:
        exec_pip(dependency)

details = 'Details\n-------\nTitle: ' + title + '\nVersion: ' + version + '\n' + 'Description: ' + description + '\n' \
          + 'Author: ' + author + '\n' + 'Author\'s Email: ' + author + '\n'

if download_url:
    details += 'Download URL: ' + download_url + '\n'

if len(dependencies) > 0:
    details += '\nDependencies:\n'
    for dependency in dependencies:
        details += dependency + '\n'

sys.stdout.write('\nquick setup finished\n\n' + details)
save_details = input("\nsave details to INFO.txt ? [y/n]: ")
save_details = save_details.lower()

if len(save_details) > 0:
    if save_details[0] == 'y':
        with open('INFO.txt', 'w+') as f:
            f.write(details)

sys.stdout.write("\nfinished\n")
