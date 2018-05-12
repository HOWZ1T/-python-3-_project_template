'''
This setup file is responsible for the general setup of the project.
'''
import subprocess
import time
import sys
import os

null_stream = None  # try and setup a DEVNULL stream for unwanted output
try:
    from subprocess import DEVNULL
    null_stream = DEVNULL
except ImportError:
    try:
        null_stream = open(os.devnull, 'wb')
    except FileNotFoundError:
        null_stream = sys.stdout
    except Exception:
        null_stream = sys.stdout


title = "Python 3 Project Template"
version = '0.0.0'
author = 'Dylan Randall'
email = 'dylan.d.randall@gmail.com'
last_updated = '12/05/2018'
min_compatible_version = (3, 6)
pip_version = 'python3'

# [module_name, version_sum] , if version_sum is -1 -> gets latest
dependencies = [['requests', '-1'], ['python-twitter', '==3.4.1']]

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

sys.stdout.write("checking dependencies...\n")
missing_dependencies = []
for dependency in dependencies:
    try:
        if dependency[1] == '-1':
            subprocess.check_call([pip_version, '-m', 'pip', 'show', dependency[0]], stdout=null_stream, stderr=null_stream)
            sys.stdout.write(dependency[0] + "...OK\n")
        else:
            subprocess.check_call([pip_version, '-m', 'pip', 'show', dependency[0] + dependency[1]], stdout=null_stream, stderr=null_stream)
            sys.stdout.write(dependency[0] + "...OK\n")
    except subprocess.CalledProcessError as e:
        missing_dependencies.append(dependency)
        sys.stdout.write(dependency[0] + "...BAD\n")
    except Exception as e:
        sys.stderr.write(str(e))
        sys.exit(-1)

time.sleep(0.1)  # wait for subprocess to finish printing
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
                        subprocess.check_call([pip_version, '-m', 'pip', 'install', module[0]])
                        missing_dependencies.remove(module)
                    else:
                        subprocess.check_call([pip_version, '-m', 'pip', 'install', module[0] + module[1]])
                        missing_dependencies.remove(module)
                except subprocess.CalledProcessError as e:
                    if e.returncode == 1:  # ignoring the upgrade pip version error
                        missing_dependencies.remove(module)
                    else:
                        sys.stderr.write('\n{}\nfailed to install module {} !\n'.format(e, module[0]))

# print final details
time.sleep(0.1)  # wait for subprocess to finish printing
success = 1
sys.stdout.write("\n\nDetails\n-------\nTitle: {}\nAuthor: {}\nEmail: {}\nLast Updated: {}\n".format(title, author,
                                                                                             email, last_updated))
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


# TODO VENV SETUP
# TODO FIX KNOWN BUG WINERROR 2 .... RELATED TO SUBPROCESS, FIND BUG HERE: https://bugs.python.org/issue17023
