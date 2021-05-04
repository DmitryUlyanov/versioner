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

        version = (
            version
            + "_torch"
            + torch.__version__.replace("+", "_")
            + f"_cu{torch.version.cuda}"
        )

    return version


def get_nvcc_version():
    p_out = (
        subprocess.check_output(["nvcc", "--version", "|", "grep", "release"])
        .strip()
        .decode()
    )
    build, version = p_out.split(",")[1].strip().split()

    assert build == "release"

    return version
