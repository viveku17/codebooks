import os
import subprocess
import tempfile


WORKSPACE = os.path.join(tempfile.gettempdir(), "CodeBooks")
REPOS_DIR = os.path.join(WORKSPACE, "Repos")
PROJECTS_DIR = os.path.join(WORKSPACE, "Projects")

def init():
    for path in (WORKSPACE, REPOS_DIR, PROJECTS_DIR):
        if not os.path.exists(path):
            os.mkdir(path)

def clone_repo(url):
    # print(f"cd {REPOS_DIR} && git clone {url}")
    subprocess.run(f"cd {REPOS_DIR} && git clone {url}")
