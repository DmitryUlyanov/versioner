import subprocess
from datetime import datetime


def build_version(include_torch=False):
    last_git_commit_hash = (
        subprocess.check_output(["git", "log", "-1", "--format=%h"]).strip().decode()
    )
    last_git_commit_date = (
        subprocess.check_output(["git", "log", "-1", "--format=%ct"]).strip().decode()
    )

    version = (
        datetime.fromtimestamp(int(last_git_commit_date)).strftime("%y.%m.%d")
        + f"+{last_git_commit_hash}"
    )
    if include_torch:
        import torch

        version = version + "_torch" + torch.__version__.replace("+", "_")

    return version
