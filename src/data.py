import os
import tempfile

WORKSPACE = os.path.join(tempfile.gettempdir(), "CodeBooks")
REPOS_DIR = os.path.join(WORKSPACE, "Repos")
PROJECTS_DIR = os.path.join(WORKSPACE, "Projects")


DATA = {
    "Workspace": WORKSPACE,
    "Repos" : REPOS_DIR,
    "Projects" : PROJECTS_DIR,
    "ActiveRepo": "",
    "ActiveBranch": ""
}


def get_data(key):
    return DATA[key]

def set_data(key, value):
    if not key in DATA:
        raise KeyError
    DATA[key] = value
