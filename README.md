# python-template
A Python template to kickstart simple projects. Whether this is a one off script, testing an idea, or a basic analysis just you will need you can use this template.

Simply clicking on a file will start the setup process and your hardware and software spec will be recorded (to help with replication and debugging), formatting tools will be included, and a virtual environment will be setup.

For projects that are intended or could be shared with others look at the shared code Python template. That template has a few additional features to make sure your code can be used by others. For larger projects there is a software template, that is for creating a tool that will be in regular use, perhaps even beyond your research group.


## Use

This template is setup so that you can simply clone or download it and double click on a file and the environment will be setup for you, including a virtual environment (venv).
Once it has installed all the dependencies you can then get started with your project. The spec of your computer has been recorded and the venv has been setup for you to run your code with.

_-_-_For Windows_-_-_
Use the .bat batch file, double click or execute from the terminal.

To enter the venv to begin installing requirements for your project type
".venv/scripts/activate" and you can continue with your regular pip installs or you can use UV to install with "uv add [project name]"

_-_-_For Linux & Mac_-_-_
Use the .sh bash file, run this from the bash terminal.

To enter the venv to begin installing requirements for your project type
"./.venv/bin/activate" and you can continue with your regular pip installs or you can use UV to install with "uv add [project name]"

_-_-_General_-_-_
When committing the pre-commit checks (for formaating, readability, and safety) will run, some of these issues can be fixed for you automatically and the changes will need to be staged again, others require a bit of manual fixing.

If you want to skip a line when formatting, add ‘# fmt: skip’ to the end of that line. For code blocks, wrap them in ‘# fmt: off’ and ‘# fmt: on’.


## Notes

Currently this template is only valid for Python 3.11 due to needing distutils (removed in 3.12) for the GPU check. We will look into a fix for this so that upto 3.13 can be used.

The ability to double click on the .sh file wil be setup in the future to provide the same ease of use for Mac & Linux users.
