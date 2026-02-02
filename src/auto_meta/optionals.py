import glob
import json
import os
import re
import tomllib

from git import Repo

# Generating the optional values that can be automatically made
# Check if optional is True
# DOI = "" # it can be automated with the zenondo library
# URL = "" # can this be auto?
# Platform = "" # can this be auto?
# Contributors = [] # commit authors can be checked, but is not certain
# Roles = {}
# Organisation = ""
# # Choose from Alpha, Beta, Production/Stable, Mature, & Inactive
# Development_status = ""


# [Software.auto]
# # These will be automatically filled out as described
# ## However, you can also manually fill them out as you see fit
# ### Just be aware that you will also need to set "auto = False"

# auto = True
# Programming_langs = [] # run a check on all the file types
# License = "" # Taken from the License file in the main folder
# Release_date = "" # time package
# Contact_person = "" # Take from the git email


def get_contributors(max_commits=800):
    # The info is extracted from across all commits
    # Open the metadata folder to get the current contrib list and lastest date
    with open(
        os.path.join(os.getcwd(), "software_metadata_template.toml"), "rb"
    ) as f:  # noqa: E501
        data = tomllib.load(f)
    contributors = data["Software"]["manual"]["Contributors"]
    # Marker must be left to say which have been checked (date range)
    # Initialize the repository object - this connects to the git repo
    repo = Repo(search_parent_directories=True)
    # Iterate through commits starting from the most recent (HEAD)
    # max_count limits how many commits we process to avoid overwhelming data

    for commit in repo.iter_commits(max_count=max_commits):
        if str(commit.committed_datetime) == data["Basic"]["Latest_commit"]:
            contributors = list(set(contributors))
            return contributors
        else:
            contributors.append(
                f"{commit.author.name}, <{commit.author.email}>"
            )

    contributors = list(set(contributors))

    return contributors


def get_url():
    # Path to the local git repository
    # repo_path = "/path/to/your/repo"
    # Initialise the Repo object
    repo = Repo(search_parent_directories=True)
    # Extract the Git repository URL
    repo_url = repo.remotes.origin.url

    return repo_url


def get_platform():
    # Open up the metadata and use the url value
    with open(
        os.path.join(os.getcwd(), "software_metadata_template.toml"), "rb"
    ) as f:  # noqa: E501
        data = tomllib.load(f)
    url = data["Software"]["manual"]["URL"]

    platform = re.findall(r"\/(\w+).", url)[0]

    return platform


def get_langs():
    # The whole project needs to be spidered
    # Check each file type against this dict
    with open(os.path.join(os.getcwd(), "languages.json")) as file:
        lang_dict = json.loads(file.read())

    # Go to parent folder and recursively glob to get all files
    files_list = glob.glob("**", root_dir=os.getcwd(), recursive=True)
    lang_list = []
    for file in files_list:
        try:
            lang_list.append(lang_dict["." + file.split(".")[-1]])
        except Exception as e:
            print(e)
    lang_list = set(lang_list)

    return lang_list


def get_license():
    # Check for license file and take the type from the first line
    try:
        with open(os.path.join(os.getcwd(), "LICENSE")) as file:
            license = file.readlines()
        return license[0].split("\n")[0]
    except FileNotFoundError:
        print("""There is no license for this project.
              That will make publishing and sharing your work difficult.""")
        return None


def get_release_date():
    repo = Repo(search_parent_directories=True)
    # repo = Repo(repo_path)

    # Get the latest tag (most recent one)
    latest_tag = repo.tags.sort(key=lambda x: x.commit.committed_datetime)[-1]

    # Get the commit associated with the tag
    commit = latest_tag.commit

    # Get the date of the commit
    release_date = commit.committed_datetime
    return release_date


def get_contact():
    # Open up repo object and take the email of the most recent commit maker
    repo = Repo(search_parent_directories=True)
    for commit in repo.iter_commits(max_count=1):
        contact = commit.author.email

    return contact
