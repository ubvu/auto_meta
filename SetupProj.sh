#! /bin/bash

# Check if UV is installed
#if [ ! -f "~/.local/bin/uv"]; then
if test -e "/usr/local/bin/uv" && [ "$(uname -s)" = "Linux" ] || [ "$(uname -p)" = "Darwin" ]; then
    echo "UV is already installed, skipping step..."
else
    # If not then install it
    if curl -LsSf https://astral.sh/uv/install.sh | sh; then
        echo "Installation succeeded"
    elif wget -qO- https://astral.sh/uv/install.sh | sh; then
        echo "Installation succeeded"
    else
        echo "Failed to install Astral"
    fi
fi;
# Add the new path to PATH as it is not done on its own
export PATH="$HOME/.local/bin:$PATH"
# Now invoke it to create a venv
uv venv --python 3.11.6
# Activate the venv
source ./.venv/bin/activate
# Initialise project (create toml, etc), needed to create this template
uv init
# Make the venv install everything from requirements.txt
uv add -r requirements.txt
pre-commit install
python get_spec.py
# Patch to make sure pip is installed in the venv
python -m ensurepip --default-pip
# Deactivate venv to ensure pip install and reactivate
deactivate
source .venv/bin/activate
