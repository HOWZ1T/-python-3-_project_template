import subprocess
import sys
import os

try:
    import pip
except ImportError:
    sys.stderr.write('Please install pip and then re-run this script.\nFor installation instructions visit: ' +
                     'https://pip.pypa.io/en/stable/installing/\n')
    sys.exit(7)


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


def check_version(min_version, max_version=None):
    sys_version = sys.version_info

    if max_version is None:
        if sys_version >= min_version:
            sys.stdout.write('Python version: {}...OK\n'.format(sys.version))
        else:
            sys.stderr.write('Python version: {}...BAD\nThis version does not meet the minimum version of: {}\n'.format(
                sys.version, min_version))
            sys.exit(5)
    elif min_version > max_version:
        sys.stderr.write('Setup configuration error!\nminimum version cannot exceed maximum version!\n')
        sys.exit(6)
    else:
        if sys_version < min_version:
            sys.stderr.write('Python version: {}...BAD\nThis version does not meet the minimum version of: {}\n'.format(
                sys.version, min_version))
            sys.exit(5)
        elif sys_version > max_version:
            sys.stderr.write('Python version: {}...BAD\nThis version exceeds the maximum version of: {}\n'.format(
                sys.version, max_version))
            sys.exit(7)
        else:
            sys.stdout.write('Python version: {}...OK\n'.format(sys.version))


title = 'Python 3 Project template'
description = 'A project template for python 3'
author = 'Dylan David Randall'
author_email = 'dylan.d.randall@gmail.com'
version = '0.0.0'
download_url = ''
min_version = (3, 0, 0)
max_version = (3, 9, 9)

dirs = ['logs']
packages = ['injection', 'logger']
modules = ['definitions.py', 'dependencies.txt']


logo = '#----------------------------------------------------------------#\n'
logo += '|      ____        _      _       _____      _                   |\n'
logo += '|     / __ \      (_)    | |     / ____|    | |                  |\n'
logo += '|    | |  | |_   _ _  ___| | __ | (___   ___| |_ _   _ _ __      |\n'
logo += '|    | |  | | | | | |/ __| |/ /  \___ \ / _ \ __| | | | \'_ \     |\n'
logo += '|    | |__| | |_| | | (__|   <   ____) |  __/ |_| |_| | |_) |    |\n'
logo += '|     \___\_\\\__,_|_|\___|_|\_\ |_____/ \___|\__|\__,_| .__/     |\n'
logo += '|                                                     | |        |\n'
logo += '|                                                     |_|        |\n'
logo += '|                                                                |\n'
logo += '#----------------------------------------------------------------#\n'
logo += '|    By Dylan Randall                                            |\n'
logo += '#----------------------------------------------------------------#'

print(logo)
save_details = input("\nsave details to INFO.txt ? [y/n]: ")
save_details = save_details.lower()

sys.stdout.write('\nchecking python version...\n')
check_version(min_version, max_version)

sys.stdout.write('\nchecking project structure...\n')
check_project_structure(modules, packages, dirs)

dependencies = parse_dependencies()
if len(dependencies) > 0:
    sys.stdout.write('\nsetting up dependencies... (this may take some time)\n')
    for dependency in dependencies:
        exec_pip(dependency)

details = 'Details\n-------\nTitle: ' + title + '\nVersion: ' + version + '\n' + 'Description: ' + description + '\n'\
          + 'Author: ' + author + '\n' + 'Author\'s Email: ' + author + '\n'

if download_url:
    details += 'Download URL: ' + download_url + '\n'

if len(dependencies) > 0:
    details += '\nDependencies:\n'
    for dependency in dependencies:
        details += dependency + '\n'

sys.stdout.write('\nquick setup finished\n\n' + details)

if len(save_details) > 0:
    if save_details[0] == 'y':
        with open('INFO.txt', 'w+') as f:
            f.write(details)

sys.stdout.write("\nfinished\n")
