import os


# ABSOLUTE RESOURCE PATHS
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # project root path
LOG = os.path.join(ROOT_DIR, "logs/")  # path for project log files
ERR_LOG = os.path.join(LOG, "errors.log")  # path to error log
INFO_LOG = os.path.join(LOG, "info.log")  # path to info / general log


def get_resource(resource_name):
    if resource_name is None:
        raise Exception("resource_name cannot be None")

    resource_name = resource_name.lower()

    if resource_name == "root":
        return ROOT_DIR
    elif resource_name == "log":
        return LOG
    elif resource_name == "error log":
        return ERR_LOG
    elif resource_name == "info log":
        return INFO_LOG

    raise Exception("resource " + resource_name + " not found")
