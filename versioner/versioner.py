import subprocess
import shutil
from datetime import datetime


def is_git_repo(root_dir) -> bool:
    return shutil.which("git") is not None and subprocess.check_output(f"git status 2>/dev/null", cwd=root_dir) == 0


def build_version(include_torch=False, root_dir="."):
    if is_git_repo(root_dir=root_dir):
        version_hash = (
            subprocess.check_output(["git", "log", "-1", "--format=%h"], cwd=root_dir).strip().decode()
        )
        last_git_commit_date = (
            subprocess.check_output(["git", "log", "-1", "--format=%ct"], cwd=root_dir).strip().decode()
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
