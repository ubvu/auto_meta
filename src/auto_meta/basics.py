import os
import re
import subprocess
from os.path import dirname, isdir, join

from git import Repo

# Automating filling out of the basics of a metadata file
# Type = "" # Pre filled based on which template is used
# Title = "" # Taken directly from the project folder name
# Description = "" # Copied from the readme
# Version = "" # Get it from the commit message if possible


def get_title():
    return os.path.basename(os.getcwd())


def get_description():
    # TODO: Fix to use relative location for the readme as cwd might not be the base folder # noqa: E501
    with open(os.path.join(os.getcwd(), "README.md")) as f:
        for line in f.readlines():
            paragraph = re.match(r"^[^#\n].+$", line)
            if len(paragraph) > 0:
                return paragraph


version_re = re.compile("^Version: (.+)$", re.M)


def get_version():
    # Try from tags
    d = dirname(__file__)
    version = ""
    if isdir(join(d, ".git")):
        # Get the version using "git describe".
        cmd = "git describe --tags --match [0-9]*".split()
        try:
            version = subprocess.check_output(cmd).decode().strip()
        except subprocess.CalledProcessError:
            print("Unable to get version number from git tags")
            exit(1)

        # PEP 386 compatibility
        if "-" in version:
            version = ".post".join(version.split("-")[:2])

        # Don't declare a version "dirty" merely because a time stamp has
        # changed. If it is dirty, append a ".dev1" suffix to indicate a
        # development revision after the release.
        with open(os.devnull, "w") as fd_devnull:
            subprocess.call(
                ["git", "status"], stdout=fd_devnull, stderr=fd_devnull
            )

        cmd = "git diff-index --name-only HEAD".split()
        try:
            dirty = subprocess.check_output(cmd).decode().strip()
        except subprocess.CalledProcessError:
            print("Unable to get git index status")
            exit(1)

        if dirty != "":
            version += ".dev1"

    # else:
    #     # Extract the version from the PKG-INFO file.
    #     with open(join(d, "PKG-INFO")) as f:
    #         version = version_re.search(f.read()).group(1)

    if version == "":
        # try from commit messages
        repo = Repo(search_parent_directories=True)
        # sha = repo.head.object.hexsha
        # repo = Repo(self.rorepo.working_tree_dir)
        # last_five_commits = list(repo.iter_commits("master", max_count=5))
        headcommit = repo.head.commit
        commit_msg = headcommit.message
        version = re.findall(r"[vV](\d*.*\d*.*\d*)", commit_msg)[0]

    return version


# print(f"pwd: {os.getcwd()}")
# print(f"rpoj name is: {)}")
