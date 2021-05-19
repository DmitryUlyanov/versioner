import subprocess
import shutil
from datetime import datetime
import os.path


def is_git_repo() -> bool:
    return shutil.which("git") is not None and os.path.isdir(".git")


def build_version(include_torch=False):
    if is_git_repo():
        version_hash = (
            subprocess.check_output(["git", "log", "-1", "--format=%h"]).strip().decode()
        )
        last_git_commit_date = (
            subprocess.check_output(["git", "log", "-1", "--format=%ct"]).strip().decode()
        )
        version_date = datetime.fromtimestamp(int(last_git_commit_date))
    else:
        version_date = datetime.now()
        version_hash = "devel"

    version_date = (
        version_date.strftime("%y.%m.%d")
        + f"+{version_hash}"
    )

    if include_torch:
        import torch

        version_date = (
            version_date
            + "_torch"
            + torch.__version__.replace("+", "_")
            + f"_cu{torch.version.cuda}"
        )

    return version_date


def get_nvcc_version():
    p_out = (
        subprocess.check_output(["nvcc", "--version", "|", "grep", "release"])
            .strip()
            .decode()
    )
    build, version = p_out.split(",")[1].strip().split()

    assert build == "release"

    return version
