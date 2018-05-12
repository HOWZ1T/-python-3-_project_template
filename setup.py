'''
This setup file is responsible for the general setup of the project.
'''
import subprocess
import time
import sys
import os


author = 'Dylan Randall'
email = 'dylan.d.randall@gmail.com'
last_updated = '12/05/2018'
min_compatible_version = (3, 6)
dependencies = [['requests', '-1']]  # [module_name, version_sum] , if version_sum is -1 -> gets latest

packages = ['injection', 'logger']
modules = ['definitions']

in_virtualenv = hasattr(sys, 'real_prefix')
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # project root path

sys.stdout.write("checking python version...\n")
if sys.version_info < min_compatible_version:
    sys.stderr.write("python version is below minimum compatible version for this project!\n")
    min_v = ""
    for v in min_compatible_version:
        min_v += str(v) + "."

    min_v = min_v[:-1]
    sys.stderr.write("current_version: {}\nminimum required version: {}\n".format(sys.version, min_v))
    sys.exit(1)

sys.stdout.write("python: {}...OK\n".format(sys.version))

sys.stdout.write("checking internal packages...\n")
for package in packages:
    path = os.path.join(ROOT_DIR, package)
    if not os.path.exists(path):
        sys.stderr.write("Missing internal package: " + package + " !\n")
        sys.exit(2)

    if not os.path.isdir(path):
        sys.stderr.write("Invalid internal package path: " + path + " is not a directory!\n")
        sys.exit(3)

    path_to_init = os.path.join(path, '__init__.py')
    if not os.path.exists(path_to_init):
        sys.stderr.write("Missing __init__.py for internal package: " + package + " !\n")
        sys.exit(4)

    if not os.path.isfile(path_to_init):
        sys.stderr.write("Invalid __init__.py for internal package: " + package + " !\n")
        sys.exit(5)

    sys.stdout.write(package + "...OK\n")
sys.stdout.write("internal packages...OK\n")


sys.stdout.write("checking internal modules...\n")
for module in modules:
    path = os.path.join(ROOT_DIR, module+".py")
    if not os.path.exists(path):
        sys.stderr.write("Missing internal module: " + module + " !\n")
        sys.exit(6)

    if not os.path.isfile(path):
        sys.stderr.write("Invalid internal module path: " + path + " is not a file!\n")
        sys.exit(7)

    sys.stdout.write(module + "...OK\n")
sys.stdout.write("internal modules...OK\n")


missing_dependencies = []
available_modules = []
lib_roots = []  # library root paths
sys.stdout.write("getting library paths...\n")
for path in sys.path:
    if os.path.isdir(path):
        end_dir = path.split('\\')
        end_dir = end_dir[-1:][0]
        if end_dir == 'lib' or end_dir == 'site-packages':
            lib_roots.append(path)
            sys.stdout.write(path + "...OK\n")

sys.stdout.write("getting available modules...\n")
skip = ['__init__', '__pycache__', 'test', 'readme', '_version', '_utils', '_main', '_monitor', '_collections',
        'top_level', 'metadata', 'installer', 'commands', 'record', '_installed', '__main__', 'make_mode']
for lib_root in lib_roots:
    for root, dirs, files in os.walk(lib_root, topdown=False):
        for name in files:
            if name is None or name == '' or name[0] == '_':
                continue

            parts = name.split('.')
            if len(parts) > 1:
                name = parts[0]

            parts = name.split('-')
            if len(parts) > 1:
                name = parts[0]

            name = name.lower()
            if name not in skip and name not in available_modules:
                available_modules.append(name)
        for name in dirs:
            if name is None or name == '' or name[0] == '_':
                continue

            parts = name.split('.')
            if len(parts) > 1:
                name = parts[0]

            parts = name.split('-')
            if len(parts) > 1:
                name = parts[0]

            name = name.lower()
            if name not in skip and name not in available_modules:
                available_modules.append(name)
sys.stdout.write("got {} possible modules\n".format(len(available_modules)))
sys.stdout.write("checking dependencies...\n")
for dependency in dependencies:
    if dependency[0].lower() in available_modules:
        sys.stdout.write(dependency[0] + "...OK\n")
    else:
        sys.stdout.write(dependency[0] + "...BAD\n")
        missing_dependencies.append(dependency)

if len(missing_dependencies) > 0:
    sys.stdout.write("missing {} dependencies\n".format(len(missing_dependencies)))
    try_install = input("attempt to install? [y/n]: ")
    try_install = try_install.lower()[0]

    if try_install == 'y':
        if in_virtualenv:
            # TODO TRY INSTALL DEPENDENCY INTO VENV
            pass
        else:
            for module in missing_dependencies:
                try:
                    if module[1] == '-1':
                        subprocess.check_call(['python', '-m', 'pip', 'install', module[0]])
                        missing_dependencies.remove(module)
                    else:
                        subprocess.check_call(['python', '-m', 'pip', 'install', module[0] + module[1]])
                        missing_dependencies.remove(module)
                except Exception as e:
                    sys.stderr.write('\n{}\nfailed to install module {} !\n'.format(e, module[0]))

# print final details
time.sleep(0.1)  # wait for subprocess to finish printing
success = 1
sys.stdout.write("\n\nAuthor: {}\nEmail: {}\nLast Updated: {}\n".format(author, email, last_updated))
if len(missing_dependencies) > 0:
    success = 0
    sys.stdout.write("missing {} dependencies:\n".format(len(missing_dependencies)))
    for module in missing_dependencies:
        if module[1] == '-1':
            sys.stdout.write('    -{}\n'.format(module[0]))
        else:
            sys.stdout.write('    -{}{}\n'.format(module[0], module[1]))

if success == 1:
    sys.stdout.write("\nsuccessfully setup project environment\n")

sys.stdout.write("\nfinished\n")
