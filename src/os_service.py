import os
import git
import subprocess

from src.data import get_data, set_data

def init():
    for path in (get_data("Workspace"), get_data("Repos"), get_data("Projects")):
        if not os.path.exists(path):
            os.mkdir(path)


def run_command(command, **kwargs):
    return subprocess.run(command.split(" "), **kwargs)


def is_git_repo(path):
    try:
        if path is not None:
            git.Repo(path).git_dir
            result = run_command(f"cd {path} && git status --porcelain", shell=True, capture_output=True)
            result_stdout = result.stdout.decode("utf-8").strip()
            return "" == result_stdout
    except Exception:
        import traceback; traceback.print_exc()
        pass
    return False


def clone_repo(url):
    repo_directory = os.path.join(get_data("Repos"), url.split("/")[-1].split(".")[0])
    if not os.path.exists(repo_directory):
        run_command(f"cd {get_data('Repos')} && git clone {url}", shell=True)
    result = is_git_repo(repo_directory)
    if result:
        set_data("ActiveRepo", repo_directory)
    return result


def get_active_repo():
    return git.Repo(get_data("ActiveRepo"))


def get_active_repo_branches():
    branches = set()
    for branch in get_active_repo().refs:
        branch_name = str(branch.name).split("/")[-1]
        if "HEAD" not in branch_name:
            branches.add(branch_name)
    return list(branches)
